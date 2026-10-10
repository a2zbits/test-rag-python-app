from dataclasses import dataclass

from app.core.config import get_settings
from app.services.embeddings import EmbeddingService
from app.services.vector_store import VectorStore


@dataclass(frozen=True)
class RetrievedChunk:
    """Structured retrieval result, ready for citation and prompt building."""

    score: float
    chunk_id: str
    document_id: str
    document_name: str
    chunk_index: int
    page_number: int | None
    section: str | None
    text: str


def retrieve(
    query: str,
    embedder: EmbeddingService,
    store: VectorStore,
    top_k: int | None = None,
    score_threshold: float | None = None,
) -> list[RetrievedChunk]:
    if not query or not query.strip():
        raise ValueError("Query must not be empty")
    settings = get_settings()
    k = top_k if top_k is not None else settings.retrieval_top_k
    if k <= 0:
        raise ValueError("top_k must be positive")
    threshold = score_threshold if score_threshold is not None else settings.retrieval_score_threshold

    vector = embedder.embed_text(query.strip())
    hits = store.search(vector, top_k=k, score_threshold=threshold)
    return [
        RetrievedChunk(
            score=h.score,
            chunk_id=h.chunk_id,
            document_id=h.payload["document_id"],
            document_name=h.payload["document_name"],
            chunk_index=h.payload["chunk_index"],
            page_number=h.payload.get("page_number"),
            section=h.payload.get("section"),
            text=h.payload["text"],
        )
        for h in hits
    ]
