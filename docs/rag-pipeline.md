# RAG Pipeline

The approved RAG pipeline for the Company Knowledge Assistant. Source: `MASTER_PLAN.md` Sections 6–8, 16–19, 31.

## Pipeline

```text
Document
    ↓
Parse            (PyMuPDF for PDF)
    ↓
Clean
    ↓
Chunk
    ↓
Attach Metadata
    ↓
Generate Embeddings
    ↓
Store in Qdrant
    ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
User Question
    ↓
Generate Query Embedding
    ↓
Semantic Retrieval (Qdrant similarity search)
    ↓
Retrieve Top-K Chunks
    ↓
Optional Similarity Threshold
    ↓
Assemble Context
    ↓
Prompt LLM (OpenAI)
    ↓
Generate Grounded Answer
    ↓
Return Answer + Citations
```

## Grounding rule (confirmed)

Answers must be grounded in retrieved company documents. If the documents lack enough information, the assistant says so instead of inventing an answer, e.g.:

```text
I couldn't find information about this topic
in the available company documents.
```

## Citations (confirmed requirement)

Each chunk carries metadata identifying its origin. Planned fields (exact schema not finalized):

```python
{
    "document_id": 12,
    "document_name": "Employee Handbook.pdf",
    "page_number": 18,
    "chunk_index": 42,
    "section": "Remote Work Policy",
}
```

The UI shows the sources used for each answer (document, page, section). Final citation UX is undecided.

## Ingestion lifecycle

Upload → extract text → clean → chunk → generate embeddings → store vectors → `READY`. Whether processing is asynchronous/background is not yet decided.

## Configuration

Chunking and retrieval must be **configurable**, not hard-coded. Model/provider settings must not be scattered through the code. Candidate settings: LLM provider/model, temperature, max tokens, embedding model, Top-K, chunk size, chunk overlap, similarity threshold (final list not approved).

## Open decisions

| Item | Status |
| --- | --- |
| OpenAI LLM model | Open |
| Embedding provider/model | Open (OpenAI embeddings possible, not approved) |
| Formats beyond PDF (TXT, Markdown, DOCX) | Open |
| Chunk size / overlap | Open (example: 800 / 100, not confirmed) |
| Top-K / similarity threshold | Open (proposed: 5 / 0.70, not confirmed) |
| Streaming mechanism | Open |
| Evaluation methodology | Open |

## Excluded from V1

Hybrid BM25 search, sophisticated reranking, GraphRAG, knowledge graphs, multi-agent retrieval.
