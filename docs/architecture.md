# Architecture

High-level architecture of the Company Knowledge Assistant. Source: `MASTER_PLAN.md` Sections 9–15, 30–32. This is a **conceptual** architecture; exact deployment topology and service boundaries are not finalized.

## Overview

```text
                    ┌─────────────────────────┐
                    │       React Frontend    │
                    │  Chat │ Documents │     │
                    │       Admin Dashboard   │
                    └────────────┬────────────┘
                                 │
                              REST API
                                 │
                    ┌────────────▼────────────┐
                    │         FastAPI         │
                    │  Chat API               │
                    │  Document API           │
                    │  Admin API              │
                    └────────────┬────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
        ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
        │ RAG Engine  │   │ SQLite / DB │   │ OpenAI API  │
        └──────┬──────┘   └─────────────┘   └─────────────┘
               │
        ┌──────▼──────┐
        │   Qdrant    │
        │ Vector DB   │
        └─────────────┘
```

## Components

- **React frontend** — Bootstrap UI with React Router and Axios. Initial pages: Login, Dashboard, AI Assistant/Chat, Documents. Later: Retrieval Playground, Evaluation, Settings, Conversations.
- **FastAPI backend** — REST API with automatic OpenAPI/Swagger docs. Chat, document, and admin routes.
- **RAG engine** — ingestion, chunking, embedding, retrieval, prompt assembly, generation. See [rag-pipeline.md](rag-pipeline.md).
- **Relational database** — SQLite initially (SQLAlchemy) for documents, chunks, conversations, messages, and query logs.
- **Qdrant** — stores embedded document chunks and serves semantic search.
- **OpenAI API** — LLM (and possibly embeddings; not yet decided). Configured via environment, never hard-coded; keys are not committed.

## Proposed backend layout (not immutable)

```text
backend/
├── app/
│   ├── main.py
│   ├── api/        # chat, documents, retrieval, admin
│   ├── core/       # config, logging
│   ├── models/
│   ├── services/   # ingestion, chunking, embeddings, retrieval, generation
│   └── rag/        # pipeline, prompts, evaluation
├── tests/
├── scripts/
└── pyproject.toml
```

## Confirmed vs. open

**Confirmed:** Python + FastAPI, React + Bootstrap, Qdrant, OpenAI APIs, SQLite initially, PyMuPDF for PDFs, uv, Docker later.

**Open:** OpenAI model, embedding model, extra document formats, Qdrant deployment mode (local / Docker / Cloud), production database, authentication details (JWT proposed), streaming mechanism, Docker Compose topology, hosting provider, API route naming, SQLAlchemy schema.

## Out of scope for V1

Multi-agent, MCP server, GraphRAG, knowledge graphs, hybrid BM25, reranking, Kubernetes, microservices, Redis, Celery, Kafka, complicated OAuth, multi-tenancy, billing, real-time collaboration, mobile app.
