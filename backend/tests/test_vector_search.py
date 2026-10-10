import uuid

import pytest
from qdrant_client import QdrantClient

from app.models import Chunk, Document
from app.services.embeddings import EmbeddingService
from app.services.indexing import index_document
from app.services.retrieval import retrieve
from app.services.vector_store import (
    CollectionNotFoundError,
    VectorStore,
    VectorStoreError,
    build_payload,
    point_id,
)
from tests.fakes import DIM, FakeOpenAI


@pytest.fixture
def embedder():
    return EmbeddingService(client=FakeOpenAI())


@pytest.fixture
def store():
    return VectorStore(QdrantClient(":memory:"), collection="test")


@pytest.fixture
def doc(session):
    d = Document(name="Leave Policy", filename="leave.pdf")
    d.chunks = [
        Chunk(chunk_index=0, text="employees receive annual leave days", page_number=3, section="Leave"),
        Chunk(chunk_index=1, text="remote work requires manager approval", page_number=4),
        Chunk(chunk_index=2, text="expense reports are due monthly", page_number=5),
    ]
    session.add(d)
    session.commit()
    return d


def test_point_id_and_payload(doc):
    chunk = doc.chunks[0]
    assert point_id(chunk) == str(chunk.id)
    assert build_payload(chunk) == {
        "chunk_id": str(chunk.id),
        "document_id": str(doc.id),
        "document_name": "Leave Policy",
        "chunk_index": 0,
        "page_number": 3,
        "section": "Leave",
        "text": "employees receive annual leave days",
    }


def test_collection_config_cosine_and_size(store):
    store.ensure_collection(DIM)
    store.ensure_collection(DIM)  # idempotent
    params = store._client.get_collection("test").config.params.vectors
    assert params.size == DIM and params.distance.name == "COSINE"
    with pytest.raises(VectorStoreError, match="vector size"):
        store.ensure_collection(DIM + 1)


def test_index_and_retrieve(session, doc, embedder, store):
    assert index_document(session, doc.id, embedder, store) == 3
    assert index_document(session, doc.id, embedder, store) == 3  # idempotent
    assert store._client.count("test").count == 3

    results = retrieve("annual leave days for employees", embedder, store, top_k=2)
    assert len(results) == 2
    top = results[0]
    assert top.chunk_id == str(doc.chunks[0].id)
    assert (top.document_name, top.page_number, top.section) == ("Leave Policy", 3, "Leave")
    assert top.text == doc.chunks[0].text and top.document_id == str(doc.id)
    assert results[0].score >= results[1].score


def test_top_k_and_threshold(session, doc, embedder, store):
    index_document(session, doc.id, embedder, store)
    assert len(retrieve("annual leave", embedder, store, top_k=1)) == 1
    assert len(retrieve("annual leave", embedder, store, top_k=10)) == 3
    assert retrieve("annual leave", embedder, store, score_threshold=0.99) == []


def test_default_top_k_comes_from_settings(session, doc, embedder, store):
    index_document(session, doc.id, embedder, store)
    assert len(retrieve("leave", embedder, store)) == 3  # only 3 chunks < default 5


def test_empty_query_rejected(embedder, store):
    for bad in ["", "   "]:
        with pytest.raises(ValueError):
            retrieve(bad, embedder, store)


def test_missing_collection(embedder, store):
    with pytest.raises(CollectionNotFoundError):
        retrieve("anything", embedder, store)


def test_unknown_document(session, embedder, store):
    with pytest.raises(LookupError):
        index_document(session, uuid.uuid4(), embedder, store)


def test_document_without_chunks_indexes_nothing(session, embedder, store):
    d = Document(name="empty", filename="e.pdf")
    session.add(d)
    session.commit()
    assert index_document(session, d.id, embedder, store) == 0


def test_qdrant_unavailable():
    unreachable = VectorStore(QdrantClient(url="http://127.0.0.1:1", timeout=1, check_compatibility=False), collection="x")
    assert unreachable.is_healthy() is False
    with pytest.raises(VectorStoreError):
        unreachable.search([0.0] * DIM, top_k=1)
