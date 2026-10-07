# CLAUDE.md

Operational instructions for Claude Code sessions on **Test RAG Python App** (demo concept: Company Knowledge Assistant).

## Read first

**Before making any change, read `MASTER_PLAN.md`.** It is the canonical specification. This file only summarizes how to work; if the two ever disagree, `MASTER_PLAN.md` wins.

## Rules

- **Never modify `MASTER_PLAN.md`** unless the user has explicitly approved a specific change (see its Section 48 change-control procedure: explain the proposal, ask, wait for approval).
- **Do not silently make unresolved decisions.** If an implementation needs a decision listed under "Open decisions" below (or in MASTER_PLAN.md Sections 45/46), stop and ask the user. Do not assume a default.
- **Do not add technologies or features** outside the approved plan. Items in MASTER_PLAN.md Section 37 are out of scope for V1.
- **Work one milestone at a time** (MASTER_PLAN.md Section 36). Do not implement future milestones unless explicitly asked.
- Keep the project minimal and portfolio-oriented; prefer the simplest approach that works.
- Be token-efficient: implement and test rather than re-explaining the project; keep reports concise.
- Never commit secrets. API keys come from `.env`; only `.env.example` is committed.
- Commit only when the user asks. Use small, focused commits.

## Confirmed decisions (summary)

- Python + FastAPI, Pydantic, SQLAlchemy, SQLite initially, pytest, `.env` configuration
- **uv** for Python package/environment management
- **Qdrant** as vector database
- **OpenAI APIs** for the LLM (not Claude APIs)
- **PyMuPDF** for PDF parsing (PDF is the planned format)
- React, Bootstrap, Bootstrap Icons, React Router, Axios (no Redux initially)
- Docker/Docker Compose later, deliberately not in early milestones
- Git + public GitHub repo
- Source citations, document ingestion, and semantic retrieval are core; the assistant must refuse to invent answers when documents lack support
- Claude Code is the primary implementation tool; Cursor and MCP are not part of V1

## Open decisions (ask before assuming)

OpenAI LLM model; embedding provider/model; document formats beyond PDF; chunk size/overlap; Top-K; similarity threshold; SQLAlchemy schema; auth/JWT details; streaming mechanism; Qdrant deployment mode; production relational DB; Docker Compose topology; hosting provider; evaluation methodology; React component/page architecture; visual design; API route naming; admin dashboard metrics; sample document content; branding.

Values such as chunk 800/100, Top-K 5, threshold 0.70 are *proposed starting points only*. Make them configurable; do not hard-code them as final.

## Current status

Milestone 0 (documentation only). No application code exists yet.

## Prompt/report conventions

Expect prompts structured as OBJECTIVE / SCOPE / REQUIREMENTS / DO NOT / TESTING / COMPLETION REPORT. Honor the DO NOT list strictly. Finish with a concise completion report, including any ambiguity encountered.

## Testing

Run tests locally (`pytest` once a backend exists) and report only relevant failures. Documentation-only milestones are verified by file existence, Markdown formatting, and consistency with `MASTER_PLAN.md`.
