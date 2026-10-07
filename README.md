# Test RAG Python App

A minimal, portfolio-oriented **Company Knowledge Assistant**: a RAG application where users ask natural-language questions about (fictional) company documents and receive answers grounded in those documents, with source citations.

> **Status: planning stage (Milestone 0).** No application code has been written yet. The canonical specification is [`MASTER_PLAN.md`](MASTER_PLAN.md).

## Goal

Demonstrate practical AI engineering: Python, FastAPI, RAG, LLM integration, embeddings, vector search, document ingestion, React, testing, and AI-assisted development. A reviewer should be able to open the app, see company documents, ask a question, and get a grounded answer plus the sources used. If the documents do not contain the answer, the assistant says so rather than inventing one.

## Confirmed technology choices

| Area | Choice |
| --- | --- |
| Backend | Python, FastAPI, Pydantic, SQLAlchemy, SQLite (initially), pytest |
| Package manager | uv |
| Vector database | Qdrant |
| LLM | OpenAI APIs |
| PDF parsing | PyMuPDF |
| Frontend | React, Bootstrap, Bootstrap Icons, React Router, Axios |
| Later | Docker / Docker Compose, GitHub CI |

## Not yet decided

OpenAI model, embedding model, formats beyond PDF, chunking and retrieval parameters, auth details, streaming mechanism, Qdrant deployment mode, hosting, and evaluation methodology. See `MASTER_PLAN.md` Sections 45–46.

## Documentation

- [`MASTER_PLAN.md`](MASTER_PLAN.md) — canonical project plan
- [`CLAUDE.md`](CLAUDE.md) — instructions for Claude Code sessions
- [`docs/architecture.md`](docs/architecture.md) — high-level architecture
- [`docs/rag-pipeline.md`](docs/rag-pipeline.md) — RAG pipeline

## Roadmap

Development proceeds milestone by milestone (0–12), from project specification through backend, database, ingestion, embeddings + Qdrant, RAG engine, chat API, React UI, admin panel, evaluation, production quality, and portfolio polish. See `MASTER_PLAN.md` Section 36.

Installation, usage, screenshots, and evaluation results will be added as the project is implemented.
