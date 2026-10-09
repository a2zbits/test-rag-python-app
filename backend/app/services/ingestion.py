import logging
import uuid
from dataclasses import dataclass
from pathlib import Path

import pymupdf
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Chunk, Document, DocumentStatus
from app.services.chunking import chunk_text, clean_text

logger = logging.getLogger(__name__)

_PDF_MAGIC = b"%PDF-"


class InvalidPDFError(ValueError):
    """The supplied file is missing or is not a PDF; no Document is created."""


class IngestionError(RuntimeError):
    """Ingestion failed after the Document was created; it is marked FAILED."""


@dataclass(frozen=True)
class PageText:
    page_number: int  # 1-based
    text: str
    section: str | None = None


def validate_pdf(path: Path) -> None:
    if not path.is_file():
        raise InvalidPDFError(f"File not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise InvalidPDFError(f"Not a .pdf file: {path.name}")
    with path.open("rb") as f:
        if f.read(len(_PDF_MAGIC)) != _PDF_MAGIC:
            raise InvalidPDFError(f"Not a valid PDF (bad header): {path.name}")


def extract_pages(path: Path) -> list[PageText]:
    """Extract cleaned text page by page, skipping pages with no text."""
    pages: list[PageText] = []
    with pymupdf.open(path) as pdf:
        toc = [(page, title) for _level, title, page in pdf.get_toc(simple=True)]
        for index, page in enumerate(pdf):
            page_number = index + 1
            text = clean_text(page.get_text("text"))
            if not text:
                logger.info("No extractable text on page %d of %s", page_number, path.name)
                continue
            section = None
            for toc_page, title in toc:
                if toc_page <= page_number:
                    section = title.strip() or section
            pages.append(PageText(page_number, text, section))
    return pages


def ingest_pdf(
    session: Session,
    path: str | Path,
    *,
    name: str | None = None,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> Document:
    """Ingest a PDF into Document + Chunk rows. Synchronous and request-agnostic.

    Raises InvalidPDFError (nothing persisted) for non-PDF input, or
    IngestionError after marking the Document FAILED with no chunks stored.
    """
    path = Path(path)
    validate_pdf(path)
    settings = get_settings()
    size = chunk_size if chunk_size is not None else settings.chunk_size
    overlap = chunk_overlap if chunk_overlap is not None else settings.chunk_overlap
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Invalid chunk configuration")

    document = Document(
        name=name or path.stem, filename=path.name, status=DocumentStatus.PENDING
    )
    session.add(document)
    session.commit()
    document_id: uuid.UUID = document.id

    try:
        document.status = DocumentStatus.PROCESSING
        session.commit()

        pages = extract_pages(path)
        index = 0
        for page in pages:
            for text in chunk_text(page.text, size, overlap):
                document.chunks.append(
                    Chunk(
                        chunk_index=index,
                        text=text,
                        page_number=page.page_number,
                        section=page.section,
                    )
                )
                index += 1
        if index == 0:
            raise IngestionError("No extractable text found in PDF")

        document.status = DocumentStatus.READY
        session.commit()
    except Exception as exc:
        session.rollback()
        failed = session.get(Document, document_id)
        failed.status = DocumentStatus.FAILED
        session.commit()
        logger.exception("Ingestion failed for %s", path.name)
        if isinstance(exc, IngestionError):
            raise
        raise IngestionError(f"Failed to ingest {path.name}: {exc}") from exc

    logger.info("Ingested %s: %d chunks", path.name, index)
    return document
