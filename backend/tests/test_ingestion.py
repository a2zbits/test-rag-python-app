from pathlib import Path

import pymupdf
import pytest
from sqlalchemy import func, select

from app.models import Chunk, Document, DocumentStatus
from app.services.ingestion import IngestionError, InvalidPDFError, extract_pages, ingest_pdf


def make_pdf(path: Path, pages: list[str], toc: list[list] | None = None) -> Path:
    pdf = pymupdf.open()
    for text in pages:
        page = pdf.new_page()
        if text:
            page.insert_textbox(pymupdf.Rect(50, 50, 550, 780), text, fontsize=11)
    if toc:
        pdf.set_toc(toc)
    pdf.save(path)
    pdf.close()
    return path


@pytest.fixture
def pdf3(tmp_path):
    return make_pdf(
        tmp_path / "Leave Policy.pdf",
        ["Employees receive 25 days of annual leave.", "Remote work needs approval.", "Expenses are reimbursed monthly."],
        toc=[[1, "Leave", 1], [1, "Remote Work", 2]],
    )


def test_extract_pages_multi_page_with_sections(pdf3):
    pages = extract_pages(pdf3)
    assert [p.page_number for p in pages] == [1, 2, 3]
    assert "25 days of annual leave" in pages[0].text
    assert [p.section for p in pages] == ["Leave", "Remote Work", "Remote Work"]


def test_ingest_success(session, pdf3):
    doc = ingest_pdf(session, pdf3)
    assert doc.status == DocumentStatus.READY
    assert doc.name == "Leave Policy" and doc.filename == "Leave Policy.pdf"
    assert [c.chunk_index for c in doc.chunks] == [0, 1, 2]
    assert [c.page_number for c in doc.chunks] == [1, 2, 3]
    assert doc.chunks[0].section == "Leave"
    assert all(c.document_id == doc.id and c.text for c in doc.chunks)
    assert session.scalar(select(func.count()).select_from(Chunk)) == 3


def test_custom_name(session, pdf3):
    assert ingest_pdf(session, pdf3, name="HR Policy").name == "HR Policy"


def test_chunk_config_changes_chunk_count(session, tmp_path):
    long_text = " ".join(f"word{i}" for i in range(80))
    pdf = make_pdf(tmp_path / "long.pdf", [long_text])
    big = ingest_pdf(session, pdf, chunk_size=2000, chunk_overlap=0)
    small = ingest_pdf(session, pdf, chunk_size=100, chunk_overlap=20)
    assert len(big.chunks) == 1
    assert len(small.chunks) > 3
    assert all(len(c.text) <= 100 and c.page_number == 1 for c in small.chunks)


def test_chunks_do_not_cross_pages(session, tmp_path):
    pdf = make_pdf(tmp_path / "p.pdf", [" ".join(["alpha"] * 60), " ".join(["beta"] * 60)])
    doc = ingest_pdf(session, pdf, chunk_size=100, chunk_overlap=10)
    for c in doc.chunks:
        assert ("alpha" in c.text) == (c.page_number == 1)
        assert ("beta" in c.text) == (c.page_number == 2)
    assert [c.chunk_index for c in doc.chunks] == list(range(len(doc.chunks)))


def test_blank_pages_skipped(session, tmp_path):
    pdf = make_pdf(tmp_path / "gaps.pdf", ["first", "", "third"])
    doc = ingest_pdf(session, pdf)
    assert [c.page_number for c in doc.chunks] == [1, 3]


def test_no_text_marks_failed_without_chunks(session, tmp_path):
    pdf = make_pdf(tmp_path / "scan.pdf", ["", ""])
    with pytest.raises(IngestionError):
        ingest_pdf(session, pdf)
    doc = session.scalars(select(Document)).one()
    assert doc.status == DocumentStatus.FAILED
    assert session.scalar(select(func.count()).select_from(Chunk)) == 0


def test_corrupt_pdf_marks_failed(session, tmp_path):
    bad = tmp_path / "bad.pdf"
    bad.write_bytes(b"%PDF-1.7\nthis is not really a pdf")
    with pytest.raises(IngestionError):
        ingest_pdf(session, bad)
    assert session.scalars(select(Document)).one().status == DocumentStatus.FAILED


def test_failure_after_chunks_added_rolls_back(session, pdf3, monkeypatch):
    real_commit = session.commit

    def failing_commit():
        if any(isinstance(o, Document) and o.status == DocumentStatus.READY for o in session.dirty):
            raise RuntimeError("db exploded")
        real_commit()

    monkeypatch.setattr(session, "commit", failing_commit)
    with pytest.raises(IngestionError, match="db exploded"):
        ingest_pdf(session, pdf3)
    monkeypatch.undo()

    assert session.scalar(select(func.count()).select_from(Chunk)) == 0
    assert session.scalars(select(Document)).one().status == DocumentStatus.FAILED


@pytest.mark.parametrize("name,content", [("a.txt", b"%PDF-1.4"), ("b.pdf", b"hello"), ("missing.pdf", None)])
def test_invalid_input_rejected_without_records(session, tmp_path, name, content):
    path = tmp_path / name
    if content is not None:
        path.write_bytes(content)
    with pytest.raises(InvalidPDFError):
        ingest_pdf(session, path)
    assert session.scalar(select(func.count()).select_from(Document)) == 0


def test_invalid_chunk_config(session, pdf3):
    with pytest.raises(ValueError):
        ingest_pdf(session, pdf3, chunk_size=10, chunk_overlap=10)
    assert session.scalar(select(func.count()).select_from(Document)) == 0
