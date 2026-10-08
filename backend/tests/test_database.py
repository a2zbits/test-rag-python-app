import uuid

import pytest
from sqlalchemy import func, inspect, select
from sqlalchemy.exc import IntegrityError

from app.models import (
    Chunk,
    Conversation,
    Document,
    DocumentStatus,
    Message,
    MessageRole,
    QueryLog,
)


def test_init_creates_tables(engine):
    assert set(inspect(engine).get_table_names()) == {
        "documents",
        "chunks",
        "conversations",
        "messages",
        "query_logs",
    }


def test_document_chunk_relationship_and_uuids(session):
    doc = Document(name="Leave Policy", filename="leave.pdf")
    doc.chunks = [
        Chunk(chunk_index=0, text="a", page_number=1, section="Intro"),
        Chunk(chunk_index=1, text="b"),
    ]
    session.add(doc)
    session.commit()

    assert isinstance(doc.id, uuid.UUID)
    assert doc.status == DocumentStatus.PENDING
    assert doc.created_at and doc.updated_at
    assert [c.chunk_index for c in doc.chunks] == [0, 1]
    assert all(isinstance(c.id, uuid.UUID) and c.document_id == doc.id for c in doc.chunks)
    assert doc.chunks[1].page_number is None and doc.chunks[1].section is None
    assert doc.chunks[0].document is doc
    assert len({doc.id, *(c.id for c in doc.chunks)}) == 3


def test_deleting_document_cascades_to_chunks(session):
    doc = Document(name="n", filename="f.pdf", chunks=[Chunk(chunk_index=0, text="x")])
    session.add(doc)
    session.commit()
    session.delete(doc)
    session.commit()
    assert session.scalar(select(func.count()).select_from(Chunk)) == 0


def test_duplicate_chunk_index_rejected(session):
    doc = Document(name="n", filename="f.pdf")
    doc.chunks = [Chunk(chunk_index=0, text="a"), Chunk(chunk_index=0, text="b")]
    session.add(doc)
    with pytest.raises(IntegrityError):
        session.commit()


def test_chunk_requires_existing_document(session):
    session.add(Chunk(document_id=uuid.uuid4(), chunk_index=0, text="x"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_conversation_messages_relationship(session):
    conv = Conversation()
    conv.messages = [
        Message(role=MessageRole.USER, content="Hi?"),
        Message(role=MessageRole.ASSISTANT, content="Hello."),
    ]
    session.add(conv)
    session.commit()

    assert isinstance(conv.id, uuid.UUID)
    assert [m.role for m in conv.messages] == [MessageRole.USER, MessageRole.ASSISTANT]
    assert all(m.conversation_id == conv.id for m in conv.messages)

    session.delete(conv)
    session.commit()
    assert session.scalar(select(func.count()).select_from(Message)) == 0


def test_invalid_message_role_rejected(session):
    conv = Conversation()
    session.add(conv)
    session.flush()
    session.add(Message(conversation_id=conv.id, role="bogus", content="x"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_query_log(session):
    log = QueryLog(question="How many leave days?", latency_ms=120)
    session.add(log)
    session.commit()
    assert isinstance(log.id, uuid.UUID) and log.created_at
