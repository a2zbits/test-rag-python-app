import logging
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Chunk, Document
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore

logger = logging.getLogger(__name__)


def index_document(
    session: Session, document_id: uuid.UUID, embedder: EmbeddingService, store: VectorStore
) -> int:
    """Embed a document's chunks and upsert them into Qdrant. Returns chunk count.

    Re-running is safe: points are keyed by chunk UUID, so they are overwritten.
    """
    if session.get(Document, document_id) is None:
        raise LookupError(f"Document {document_id} not found")
    chunks = list(
        session.scalars(
            select(Chunk)
            .where(Chunk.document_id == document_id)
            .options(joinedload(Chunk.document))
            .order_by(Chunk.chunk_index)
        )
    )
    if not chunks:
        return 0
    vectors = embedder.embed_texts([c.text for c in chunks])
    store.ensure_collection(len(vectors[0]))  # dimension taken from the API response
    store.upsert_chunks(chunks, vectors)
    logger.info("Indexed %d chunks for document %s", len(chunks), document_id)
    return len(chunks)
