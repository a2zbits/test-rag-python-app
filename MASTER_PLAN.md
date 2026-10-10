# MASTER_PLAN.md
# Test RAG Python App — Canonical Project Plan

> **Status:** Implementation in progress; Milestones 0–4 completed  
> **Purpose:** Canonical source of truth for the Test RAG Python App project  
> **Last updated:** 2026-10-11  
> **Project name:** Test RAG Python App  
> **Demo application concept:** Company Knowledge Assistant

---

## 1. Purpose of This Document

This file is the canonical source of truth for the Test RAG Python App project.

It captures the implementation plan and decisions explicitly agreed upon in the project discussion so far, including:

- project goals
- intended portfolio/demo scope
- architecture
- technology choices
- RAG approach
- frontend/backend direction
- document handling
- deployment strategy
- AI-assisted development workflow
- token/usage optimization
- confirmed decisions
- proposals that have not yet been approved
- open questions
- current implementation status

### Change-control rule

This document must **not be automatically modified during future discussions**.

If a future discussion introduces a proposed change to:

- project goals
- architecture
- technology choices
- RAG approach
- approved scope
- implementation strategy
- other significant project decisions

the proposed change must first be explained to the user and receive **explicit approval**.

Only after explicit approval should `MASTER_PLAN.md` be updated.

During future implementation work, the latest approved version of this file should be treated as the primary project reference. The ongoing conversation may provide additional temporary context, but it must not silently override an approved decision in this document.

---

# 2. Project Goal

Build a **professional-looking, minimal viable RAG application** in Python that can be published as a public GitHub portfolio project.

The application should demonstrate practical competency in:

- Python
- FastAPI
- RAG
- LLM integration
- embeddings
- vector databases
- document ingestion
- prompt engineering
- ReactJS
- Bootstrap
- API design
- testing
- Docker
- Git/GitHub
- modern AI-assisted software development

The project should be:

1. small enough to finish,
2. sophisticated enough to demonstrate modern AI engineering skills,
3. understandable enough that the developer can explain the architecture in an interview,
4. visually polished enough to function as a portfolio demo,
5. useful to both technical and non-technical reviewers.

---

# 3. Demo Concept — Confirmed Decision

## Company Knowledge Assistant

The selected demo concept is **Option B — Company Knowledge Assistant**.

The application will simulate an internal company knowledge system in which users can ask questions about company documentation.

This was selected because interviewers and HR personnel may not be technical. A company-policy-oriented RAG application makes the RAG concept easy to understand and test.

A reviewer should be able to:

1. open the application,
2. see company documents,
3. ask a natural-language question,
4. receive an answer grounded in those documents,
5. see the sources used to produce the answer.

---

# 4. Example Company Documents

The planned fictional company documentation may include documents such as:

- Employee Handbook
- HR Policy
- Leave & Attendance Policy
- Remote Work Policy
- IT & Security Policy
- Engineering Handbook
- Benefits & Compensation Policy
- Code of Conduct
- Expense Policy

These are examples discussed during planning. The exact final document set has not yet been finalized.

The documents are expected to be fictional/demo material rather than real confidential company documents.

---

# 5. Primary User Experience

The main user-facing feature is an AI assistant.

Example interaction:

> **User:** How many annual leave days do employees receive?

The assistant should answer using the indexed company documents and provide source information.

Example conceptual response:

> According to the company's Leave Policy, employees receive the specified annual leave allowance subject to the policy conditions.

Then:

```text
Sources
────────────────────────
Leave Policy.pdf
Page 3

Employee Handbook.pdf
Page 18
```

The exact wording and source presentation will be implemented later.

---

# 6. Core RAG Behavior

The intended RAG pipeline is:

```text
Document
    ↓
Parse
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
    ↓
User Question
    ↓
Generate Query Embedding
    ↓
Semantic Retrieval
    ↓
Retrieve Top-K Chunks
    ↓
Optional Similarity Threshold
    ↓
Assemble Context
    ↓
Prompt LLM
    ↓
Generate Grounded Answer
    ↓
Return Answer + Citations
```

The application should not simply behave as a generic LLM chatbot.

The answer should be grounded in the retrieved company documentation.

---

# 7. Hallucination / Grounding Rule

A central RAG behavior is:

> If the available documents do not contain enough information to answer a question, the assistant should say that it cannot find sufficient information in the available company documents rather than inventing an answer.

Example:

```text
I couldn't find information about this topic
in the available company documents.
```

This is an important part of demonstrating genuine RAG behavior.

---

# 8. Source Citations — Confirmed Requirement

Answers should expose the documents/chunks used to construct the response.

Each chunk should carry sufficient metadata to identify its origin.

Planned metadata includes:

```python
{
    "document_id": 12,
    "document_name": "Employee Handbook.pdf",
    "page_number": 18,
    "chunk_index": 42,
    "section": "Remote Work Policy"
}
```

The relational database schema is approved as follows:

- `documents.id`: UUID primary key
- `chunks.id`: UUID primary key; `document_id` is a UUID foreign key to `documents.id`
- `conversations.id`: UUID primary key
- `messages.id`: UUID primary key; `conversation_id` is a UUID foreign key to `conversations.id`
- `query_logs.id`: UUID primary key; relationships should use UUID foreign keys where applicable

UUIDs are used to provide globally unique identifiers and keep the SQL ↔ Qdrant relationship clean. A Qdrant point representing a chunk should use the chunk UUID as its point identifier (or an equivalent direct UUID mapping).

The UI should eventually display information such as:

```text
Sources

Employee Handbook.pdf
Page 18
Remote Work Policy
```

The final citation UX is an implementation detail still to be determined.

---

# 9. Technology Stack — Confirmed Choices

## Backend

- **Python**
- **FastAPI**
- **Pydantic**
- **SQLAlchemy**
- **SQLite initially**
- **pytest**
- `.env`-based configuration

## Vector database

- **Qdrant**

Qdrant replaces the previously considered ChromaDB choice.

## LLM

- **OpenAI APIs**

The application should use OpenAI's APIs for LLM access rather than Claude APIs.

Reason for this decision:

- the user expects their ChatGPT subscription to remain available,
- the user's Claude subscription may expire,
- the portfolio demo should therefore not depend on the continued availability of the user's Claude subscription.

The approved OpenAI model is **GPT-5.4 mini**.

## Embeddings

- Embeddings are required.
- The approved embedding provider/model is **OpenAI `text-embedding-3-small`**.

## Document parsing

- **PyMuPDF** is the planned PDF parsing technology.

The final set of supported file formats has not yet been finalized.

## Frontend

- **ReactJS**
- **Bootstrap**
- **Bootstrap Icons**
- **React Router**
- **Axios**

ReactJS is a confirmed requirement specifically so the project can demonstrate ReactJS experience.

Bootstrap remains part of the frontend stack.

Redux is not planned initially.

## Containerization

- **Docker**
- Docker Compose is expected for the final application, but Docker is deliberately not part of the initial implementation phase.
- During development, Qdrant runs in a separate Docker container.
- On the user's Intel MacBook Pro/macOS Ventura development machine, the working Docker runtime is **Colima** rather than Docker Desktop or Lima.

## Version control

- **Git**
- **GitHub**

The final repository is intended to be public and portfolio-ready.

---

# 10. Package Management — Confirmed Decision

The project will use **uv** for Python package and environment management.

The user explicitly approved uv as the project package manager before implementation.

Do not silently change this decision in future implementation work. Any replacement package-management approach requires explicit approval.

---

# 11. Planned Architecture

The conceptual architecture is:

```text
                    ┌─────────────────────────┐
                    │       React Frontend    │
                    │                         │
                    │  Chat │ Documents │     │
                    │       Admin Dashboard   │
                    └────────────┬────────────┘
                                 │
                              REST API
                                 │
                    ┌────────────▼────────────┐
                    │       FastAPI           │
                    │                         │
                    │  Chat API               │
                    │  Document API           │
                    │  Admin API              │
                    └────────────┬────────────┘
                                 │
               ┌─────────────────┼─────────────────┐
               │                 │                 │
        ┌──────▼──────┐   ┌──────▼──────┐   ┌─────▼──────┐
        │ RAG Engine  │   │ SQLite / DB  │   │ OpenAI API │
        │             │   │              │   │             │
        └──────┬──────┘   └──────────────┘   └─────────────┘
               │
        ┌──────▼──────┐
        │   Qdrant    │
        │ Vector DB   │
        └─────────────┘
```

This is a conceptual architecture. Exact deployment topology and service boundaries remain subject to implementation.

---

# 12. Backend Project Structure — Proposed

The following structure was proposed:

```text
backend/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── chat.py
│   │   ├── documents.py
│   │   ├── retrieval.py
│   │   └── admin.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── logging.py
│   │
│   ├── models/
│   │
│   ├── services/
│   │   ├── ingestion.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retrieval.py
│   │   └── generation.py
│   │
│   └── rag/
│       ├── pipeline.py
│       ├── prompts.py
│       └── evaluation.py
│
├── tests/
├── scripts/
└── pyproject.toml
```

This is a **proposed structure**, not an immutable decision. It should be refined only with explicit approval if the architecture changes materially.

---

# 13. Frontend Project Structure — Proposed

A conceptual React structure was discussed:

```text
frontend/
├── src/
│   ├── components/
│   ├── pages/
│   ├── layouts/
│   ├── services/
│   ├── hooks/
│   ├── context/
│   ├── utils/
│   └── App.jsx
│
├── public/
└── package.json
```

The exact React architecture is not yet finalized.

---

# 14. Planned Frontend Pages

## Initial UI

The planned initial pages are:

1. Login
2. Dashboard
3. AI Assistant / Chat
4. Documents

## Later UI

Potential additional pages:

5. Retrieval Playground
6. Evaluation
7. Settings
8. Conversations

The exact page sequence may be refined during implementation, but the goal is to avoid unnecessary frontend complexity.

---

# 15. UI / UX Direction

The application should look like a small professional SaaS/internal company application rather than a basic tutorial chatbot.

Conceptual layout:

```text
┌─────────────────────────────────────────────────────────┐
│ Company Knowledge Assistant              Admin ▼        │
├───────────────┬─────────────────────────────────────────┤
│ Dashboard     │                                         │
│ Ask Assistant │          Chat Area                      │
│ Documents     │                                         │
│ Retrieval     │                                         │
│ Evaluations   │                                         │
│ Settings      │                                         │
└───────────────┴─────────────────────────────────────────┘
```

The final visual design has not yet been specified.

---

# 16. Document Management

The administrator should eventually be able to:

- upload documents,
- inspect document status,
- delete documents,
- re-index/reprocess documents.

Conceptual ingestion lifecycle:

```text
Upload
  ↓
Extract text
  ↓
Clean
  ↓
Chunk
  ↓
Generate embeddings
  ↓
Store vectors
  ↓
READY
```

A document should have a visible status such as:

```text
READY
```

The exact asynchronous/background processing design is not yet finalized.

---

# 17. Initial Document Format Scope — Open Question

PDF support is planned and PyMuPDF was selected as the planned PDF parsing technology.

Other formats discussed included:

- TXT
- Markdown
- DOCX

However, the exact V1 supported-format list has **not** been formally approved.

Do not assume all four formats must be implemented in V1 without further confirmation.

---

# 18. Chunking

Chunking is a core part of the ingestion pipeline.

Candidate configuration discussed:

```text
Chunk size: 800
Chunk overlap: 100
```

These values were examples/configuration ideas, **not confirmed final parameters**.

The implementation should make chunking configurable rather than permanently hard-code an unapproved value.

---

# 19. Retrieval

The initial retrieval design is intentionally simple:

```text
User question
    ↓
Query embedding
    ↓
Qdrant similarity search
    ↓
Top K chunks
    ↓
Optional similarity threshold
    ↓
Context assembly
```

Candidate configuration discussed:

```text
Top K = 5
Similarity threshold = 0.70
```

These are **proposed starting values**, not final approved values.

Advanced retrieval techniques such as the following are deliberately excluded from V1:

- hybrid BM25 search
- sophisticated reranking
- GraphRAG
- knowledge graphs
- multi-agent retrieval

They may be considered later if explicitly approved.

---

# 20. RAG Configuration

A settings/admin interface was proposed with parameters such as:

```text
LLM provider
LLM model
Temperature
Max tokens

Embedding model

Top K
Chunk size
Chunk overlap
Similarity threshold
```

The final list of configurable settings has not yet been approved.

---

# 21. Chat API

A core FastAPI endpoint is expected to be similar to:

```text
POST /api/chat
```

The chat system should eventually support:

- user question
- RAG retrieval
- grounded response
- citations/sources
- conversation persistence
- conversation history

Additional API routes proposed include:

```text
POST   /api/documents/upload
GET    /api/documents
DELETE /api/documents/{id}

POST   /api/retrieval/search

GET    /api/conversations
GET    /api/conversations/{id}

GET    /api/admin/stats
GET    /api/admin/logs
```

These routes are proposed and may be adjusted during implementation.

FastAPI's automatic OpenAPI/Swagger documentation should be retained as part of the backend.

---

# 22. Conversation History

A conversation model was proposed conceptually:

```text
Conversation
    ├── User message
    ├── Assistant response
    ├── Sources
    └── Timestamp
```

The UI may provide:

```text
New Conversation

Previous conversations:
- Leave policy
- Remote work
- Security requirements
- Employee benefits
```

The exact database schema and conversation UX remain implementation details.

---

# 23. Streaming Responses

Streaming responses were identified as a desirable professional feature.

The intended UX is for the assistant's response to appear progressively rather than waiting for the entire response.

The exact streaming mechanism has not yet been finalized.

---

# 24. Retrieval Playground

A retrieval-testing interface was proposed.

Conceptually:

```text
Question:
[ What is the remote work policy? ]

Top K:
[ 5 ]

Similarity threshold:
[ 0.70 ]

[ Search ]

Results

#1  Score: 0.91
Employee Handbook.pdf
Page 18

#2  Score: 0.87
Remote Work Policy.pdf
Page 3
```

This is intended to demonstrate the distinction between:

- retrieval,
- context selection,
- final answer generation.

It is a planned feature, but exact UI and implementation are not yet finalized.

---

# 25. Admin Dashboard

A dashboard was proposed with high-level system statistics such as:

```text
Documents
Chunks
Queries
Average latency
```

A possible expanded status view:

```text
API                 Online
Database            Online
Vector Store        Online
LLM                 Connected
Embedding Service   Connected
```

Exact metrics and health checks are not yet finalized.

---

# 26. Evaluation

Evaluation is an important planned feature because the goal is to demonstrate actual RAG engineering rather than merely build a chatbot.

A possible dataset:

```text
evaluation/
    questions.json
```

Example:

```json
{
  "question": "How many annual leave days do employees receive?",
  "expected_sources": [
    "Leave Policy.pdf"
  ]
}
```

Potential evaluation metrics discussed:

- retrieval accuracy
- answer relevance
- faithfulness
- average latency

A conceptual dashboard could show:

```text
Questions                 25
Retrieval accuracy        88%
Answer relevance          92%
Faithfulness              94%
Average latency           1.7 sec
```

These numbers are illustrative only and must never be presented as actual results until measured.

The exact evaluation methodology has not yet been finalized.

---

# 27. Logging and Observability

Backend logging is planned.

A conceptual query log:

```text
Timestamp
Question
Retrieved chunks
Latency
Model
```

A possible admin log view was proposed.

Exact logging implementation and retention policy remain open.

---

# 28. Authentication

A simple authentication layer was proposed.

Potential approach:

- `/login`
- JWT
- protected API routes
- protected React routes

The intention is **not** to build enterprise-grade identity management.

The exact authentication implementation has not yet been approved.

---

# 29. Database Strategy

SQLite is the planned initial relational database.

PostgreSQL was mentioned as a possible later production choice.

The initial project should avoid unnecessary infrastructure complexity.

The exact production relational database choice is **not yet finalized**.

---

# 30. Qdrant Strategy

Qdrant is the confirmed vector database.

The application should store embedded document chunks in Qdrant and retrieve semantically relevant chunks for user queries.

The approved development deployment is **Qdrant in a separate Docker container**, independent from the Python application containerization. This keeps the vector database isolated and allows the application to connect to Qdrant over its service endpoint.

The verified local development setup uses **Colima** as the Docker runtime on the user's Intel MacBook Pro running macOS Ventura. The active Docker context is `colima`; Docker Desktop is not used, and the previously configured `lima-docker` context is not the working runtime. The current development Qdrant image is pinned to `qdrant/qdrant:v1.19.2`.

Qdrant Cloud or another production deployment model may be considered later if needed, but it requires explicit approval if it materially changes architecture or cost.

---

# 31. OpenAI API Strategy

OpenAI APIs are the confirmed LLM integration choice.

The application should be designed so that the model/provider configuration is not unnecessarily hard-coded throughout the codebase.

The approved model is **GPT-5.4 mini** and the approved embedding model is **text-embedding-3-small**.

API keys must be loaded through environment configuration and must not be committed to GitHub.

A `.env.example` file is planned.

---

# 32. Docker Strategy

Docker is planned for application containerization later, but it should **not** be the first application implementation step. The approved exception is that Qdrant may run in its own separate Docker container during development.

### Verified local Docker development environment

The user's working Docker environment is: **Docker CLI 29.2.1 + Colima + Docker context `colima`** on an Intel MacBook Pro running macOS Ventura via OCLP. Colima uses macOS Virtualization.Framework with x86_64 architecture and virtiofs. Docker Desktop is not used. Lima is not the active runtime.

Typical startup/check sequence:

```text
colima start
docker context use colima
docker info
```

The Qdrant development container runs separately from the application containerization effort. Its current verified image is `qdrant/qdrant:v1.19.2`, exposed on port 6333 with persistent development storage under `./qdrant_storage/`. Qdrant 1.19.2 has been successfully started and accessed by the Python application through this setup.

Preferred sequence:

```text
Local development
       ↓
Working backend
       ↓
Working RAG
       ↓
Working React UI
       ↓
Testing
       ↓
Dockerization
       ↓
Deployment configuration
```

This is intentional to avoid debugging application problems and container problems simultaneously.

A final Docker Compose setup is expected, but the exact service topology is not yet finalized.

---

# 33. Deployment Strategy

The project should ultimately be suitable for public GitHub presentation and potentially a deployed demo.

Deployment has not yet been specified to a particular hosting provider.

The project should be prepared for:

- environment variables,
- Docker,
- production configuration,
- API/frontend separation as appropriate,
- secure handling of API keys.

A specific cloud provider and final deployment architecture are **open questions**.

---

# 34. GitHub Repository Structure — Proposed

The proposed final repository structure is:

```text
company-knowledge-assistant/
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── scripts/
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── documents/
│   └── sample/
│
├── evaluation/
│   ├── questions.json
│   └── results/
│
├── docs/
│   ├── architecture.md
│   ├── rag-pipeline.md
│   └── evaluation.md
│
├── screenshots/
│
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

This structure is proposed and may be refined during implementation.

---

# 35. GitHub README / Portfolio Requirements

The final public repository should explain:

- what the application does,
- why it exists,
- architecture,
- RAG pipeline,
- technology stack,
- local installation,
- environment configuration,
- how to run it,
- how to upload documents,
- how retrieval works,
- how citations work,
- evaluation approach,
- screenshots,
- known limitations,
- future improvements.

An architecture diagram and screenshots are planned portfolio assets.

---

# 36. Development Milestones — Approved Overall Sequence

The agreed implementation sequence is approximately:

## Milestone 0 — Project specification

Create:

- `CLAUDE.md`
- `README.md`
- architecture documentation

No substantial application implementation yet.

## Milestone 1 — Backend foundation

Implement:

- Python project
- FastAPI
- configuration
- logging
- health endpoint
- testing foundation

## Milestone 2 — Database

Implemented the initial relational models:

- Document
- Chunk
- Conversation
- Message
- QueryLog

Initial SQLAlchemy schemas are implemented with UUID-based core identifiers, timestamps, relationships, constraints, and SQLite foreign-key behavior. Future schema evolution remains possible if later milestones require it.

## Milestone 3 — Document ingestion

Implemented:

```text
PDF
 ↓
Page-by-page text extraction
 ↓
Cleaning
 ↓
Deterministic page-bounded chunking
 ↓
Metadata
 ↓
SQLite persistence
```

Implementation uses PyMuPDF, configurable character-based chunking, 1-based page numbers, optional PDF outline/section metadata, and document status transitions including failure handling.

## Milestone 4 — Embeddings + Qdrant — COMPLETED

Implemented:

```text
Chunk
 ↓
OpenAI embedding abstraction
 ↓
Qdrant
 ↓
Semantic retrieval
```

Implemented components include:

- OpenAI `text-embedding-3-small` embedding service
- batched embedding requests with order preservation
- Qdrant vector-store abstraction
- collection creation and vector-size validation
- UUID chunk IDs used as Qdrant point IDs
- citation metadata stored in Qdrant payloads
- indexing service
- retrieval service with configurable Top-K and optional score threshold
- Qdrant connectivity check
- local Qdrant startup documentation/script
- fake/in-memory tests for application-level behavior

Verification completed:

- 48 automated tests pass
- real Qdrant 1.19.2 container verified through Colima
- real collection creation, vector upsert, search, payload retrieval, and score-threshold behavior verified against Qdrant
- no real OpenAI API call was made during this milestone verification

The exact final retrieval Top-K and similarity threshold remain implementation defaults rather than permanent project decisions.

## Milestone 5 — RAG engine

Implement:

```text
Question
 ↓
Retrieval
 ↓
Context
 ↓
Prompt
 ↓
OpenAI API
 ↓
Answer + citations
```

This is the central RAG milestone.

## Milestone 6 — Chat API

Implement:

- chat endpoint
- conversation persistence
- sources/citations

## Milestone 7 — React application

Implement:

- React
- Bootstrap
- routing
- API client
- application layout
- authentication foundation

## Milestone 8 — Chat UI

Implement:

- conversation list
- chat
- streaming
- sources
- new conversation

## Milestone 9 — Admin panel

Implement:

- dashboard
- documents
- upload
- delete
- re-index
- retrieval playground

## Milestone 10 — Evaluation

Implement:

- evaluation dataset
- retrieval metrics
- answer evaluation
- evaluation UI

## Milestone 11 — Production quality

Add:

- error handling
- logging
- security
- tests
- Docker
- environment configuration
- CI

## Milestone 12 — Portfolio polish

Finalize:

- README
- architecture diagram
- screenshots
- demo data
- setup instructions
- technical explanation
- evaluation results
- future roadmap

---

# 37. Explicitly Out of Scope for V1

The following were deliberately identified as things **not to build initially**:

- multi-agent architecture
- MCP server
- GraphRAG
- knowledge graphs
- hybrid BM25 search
- sophisticated reranking
- Kubernetes
- microservices
- Redis
- Celery
- Kafka
- complicated OAuth
- multi-tenancy
- billing
- real-time collaboration
- mobile application

These can be considered for later versions only with explicit approval.

---

# 38. MCP Strategy

The user has completed MCP Introduction/Advanced training.

MCP should **not** be forced into the core V1 architecture.

A potential V2 enhancement is an MCP server exposing tools such as:

```text
search_company_documents()
get_document()
search_policy()
```

Possible future architecture:

```text
Claude / MCP Client
        │
        ▼
Company Knowledge MCP Server
        │
        ▼
RAG Backend
```

This is a future possibility, not a V1 requirement.

---

# 39. AI-Assisted Development Strategy

The project is intended to use modern AI development tools.

## Claude Code — Primary development tool

Claude Code should be the main implementation agent.

Potential uses:

- project scaffolding
- backend implementation
- RAG implementation
- testing
- debugging
- refactoring
- Git operations
- documentation
- code review

The user has Claude Code installed and has completed Claude Code 101 and Claude Code in Action training.

## Claude Cowork — Supporting tool

Cowork is intended primarily for higher-level work such as:

- research
- document preparation
- evaluation dataset preparation
- documentation review
- architecture review
- portfolio preparation

It is not intended to replace Claude Code as the primary implementation tool.

## Cursor — Optional tool

The user does not currently have a paid Cursor account and may purchase the $20 plan later.

Cursor is **not required for V1**.

The implementation should initially proceed using the existing Claude Code setup.

A Cursor subscription can be reconsidered later, particularly for React/frontend work.

---

# 40. Token / Usage Optimization Strategy — Confirmed Requirement

The implementation must be planned to consume as few AI coding-tool tokens as reasonably possible.

The agreed principles are:

### 1. Do not ask an AI coding agent to build the entire project in one prompt.

Work should be divided into focused milestones.

### 2. Use `CLAUDE.md`

The project should maintain persistent instructions covering:

- project purpose
- architecture
- technology stack
- directory structure
- coding conventions
- RAG decisions
- API conventions
- testing requirements
- things not to change

This reduces repeated explanations.

### 3. Keep prompts focused

Each implementation prompt should normally:

- have one logical objective,
- identify scope,
- identify allowed files where practical,
- specify requirements,
- specify things not to change,
- require tests,
- require a concise completion report.

### 4. Avoid unnecessary explanations

The coding agent should implement and test rather than repeatedly regenerate large explanations of the whole project.

### 5. Run tests locally

Use local commands such as:

```text
pytest
```

and provide only relevant failures to the AI coding agent when debugging.

### 6. Commit frequently

Use small Git commits so changes can be reviewed or reverted safely.

Example:

```text
git commit -m "Add document ingestion pipeline"
git commit -m "Add vector retrieval"
git commit -m "Add RAG chat endpoint"
```

### 7. Avoid unnecessary architecture exploration

The project should remain deliberately simple.

---

# 41. Future Prompting Workflow

For future implementation discussions, prompts intended for Claude Code should generally contain:

```text
OBJECTIVE

SCOPE

REQUIREMENTS

DO NOT

TESTING

COMPLETION REPORT
```

The prompt should tell Claude Code to read `CLAUDE.md` before implementation.

Prompts should normally instruct the agent not to implement future milestones unless explicitly requested.

---

# 42. Roles of the AI Tools

The intended workflow is:

```text
User
  │
  │ Focused implementation prompt
  ▼
Claude Code
  │
  ├── Inspect
  ├── Implement
  ├── Test
  └── Report
  │
  ▼
User
  │
  ├── Run application
  ├── Manual test
  └── Review Git diff
  │
  ▼
ChatGPT
  │
  ├── Architecture guidance
  ├── Prompt design
  ├── Troubleshooting
  ├── Code/architecture review
  └── Next-step planning
```

The intention is that ChatGPT acts as an architecture/engineering mentor and Claude Code acts primarily as the implementation agent.

---

# 43. Portfolio Positioning

The project is intended to demonstrate the user's transition from long-term full-stack/Laravel development toward modern AI engineering.

The portfolio story should demonstrate a progression such as:

```text
PHP / Laravel / Full-stack
        ↓
Python
        ↓
FastAPI
        ↓
Machine Learning
        ↓
LLMs
        ↓
RAG
        ↓
AI Engineering
        ↓
Agentic Development
```

ReactJS is also intentionally included so the project can demonstrate modern frontend experience alongside the Python AI stack.

The project should therefore demonstrate:

```text
Backend engineering
+
React frontend
+
RAG
+
LLMs
+
Vector search
+
AI-assisted development
=
Modern AI full-stack engineering
```

---

# 44. Confirmed Decisions

The following decisions are currently considered **approved/confirmed**:

1. The project is a professional minimal viable RAG portfolio application.
2. The demo concept is **Company Knowledge Assistant**.
3. The target audience includes non-technical interviewers/HR.
4. The frontend will use **ReactJS**.
5. The frontend will use **Bootstrap**.
6. The backend will use **Python + FastAPI**.
7. The vector database will be **Qdrant**.
8. The application will use **OpenAI APIs** for its LLM instead of Claude APIs.
9. Source citations are a core requirement.
10. Document ingestion is a core requirement.
11. Semantic retrieval is a core requirement.
12. The application should refuse to invent information when the indexed documents do not support an answer.
13. A professional admin/control panel is part of the intended application.
14. RAG evaluation is part of the intended project.
15. Docker is intended for the later production-quality stage.
16. The project will be published as a public GitHub portfolio repository.
17. Token/usage efficiency is an important development constraint.
18. Claude Code is the primary AI coding tool for implementation.
19. Claude Cowork is a supporting research/review/organization tool.
20. Cursor is optional and should not be required to start V1.
21. MCP is not required for V1.
22. The Python package/environment manager will be **uv**.
23. The OpenAI LLM model will be **GPT-5.4 mini**.
24. The embedding model will be **text-embedding-3-small**.
25. The core relational entities `documents`, `chunks`, `conversations`, and `messages` will use **UUID primary keys**; related foreign keys will use UUIDs.
26. Qdrant will run in a **separate Docker container** during development, independent from application containerization.
27. The verified local Docker runtime for development is **Colima** with Docker context `colima`; Docker Desktop and the inactive `lima-docker` context are not used.
28. The development Qdrant container is currently pinned to **`qdrant/qdrant:v1.19.2`**.

---

# 45. Proposals / Not Yet Finalized

The following were discussed but should **not** be treated as immutable decisions:

1. Exact supported document formats beyond PDF.
2. Exact chunk size.
3. Exact chunk overlap.
4. Exact Top-K retrieval value.
5. Exact similarity threshold.
6. Exact authentication/JWT implementation.
7. Exact streaming mechanism.
8. Exact relational production database.
9. Exact Docker Compose service topology for the application.
10. Exact cloud deployment provider.
11. Exact evaluation methodology and metrics.
12. Exact React component/page architecture.
13. Exact visual design.
14. Exact API route naming.
15. Exact admin dashboard metrics.

These must not be silently converted into permanent decisions.

---

# 46. Open Questions

Before or during implementation, decisions may be required for:

- Which exact V1 document formats?
- SQLite only vs PostgreSQL for deployment?
- Which hosting provider, if deployment is pursued?
- Exact authentication mechanism?
- Exact streaming mechanism?
- Exact evaluation methodology?
- Exact sample company/document content?
- Exact application branding/name?
- Whether the final project should include a live public demo?
- Whether Cursor should be added later?

These should be resolved deliberately rather than assumed.

---

# 47. Current Implementation Status

## Overall

**Implementation is in progress. Milestones 0, 1, 2, 3, and 4 are completed and committed. Milestone 5 is the next implementation milestone.**

The canonical plan remains the source of truth for approved architecture and open decisions. Actual implementation status below reflects the reviewed repository state as of 2026-10-11.

## Completed Milestones

### Milestone 0 — Project specification — COMPLETED

Created and reviewed the initial project specification artifacts, including:

- `CLAUDE.md`
- `README.md`
- `docs/architecture.md`
- `docs/rag-pipeline.md`

The canonical `MASTER_PLAN.md` was preserved as the approved source of truth.

### Milestone 1 — Backend foundation — COMPLETED

Implemented:

- Python backend project managed with `uv`
- FastAPI application
- environment configuration with Pydantic Settings
- logging foundation
- `/api/health` endpoint
- pytest/httpx testing foundation
- `.env.example` and project `.gitignore` configuration

Verification: health endpoint and backend tests passed; the milestone was committed.

### Milestone 2 — Database — COMPLETED

Implemented:

- SQLAlchemy database foundation
- SQLite initial database
- UUID/timestamp mixins
- `Document` model
- `Chunk` model
- `Conversation` model
- `Message` model
- `QueryLog` model
- relationships, cascading behavior, and relevant constraints
- database initialization script
- database tests

Verification: database and health tests passed; the milestone was committed. Runtime SQLite database files remain ignored by Git.

### Milestone 3 — Document ingestion — COMPLETED

Implemented:

- PDF parsing with PyMuPDF
- page-by-page extraction
- text cleaning
- hyphenated line handling
- whitespace/paragraph normalization
- deterministic character-based chunking
- configurable chunk size and overlap
- page-bounded chunks
- page and optional section metadata
- document status transitions and failure handling
- persistence of documents and chunks

Verification: 32 tests passed at milestone completion; the milestone was committed.

### Milestone 4 — Embeddings + Qdrant — COMPLETED

Implemented:

- OpenAI `text-embedding-3-small` embedding service
- batched embedding requests and order preservation
- Qdrant vector-store abstraction
- cosine similarity collection configuration
- collection/vector-size validation
- UUID chunk IDs mapped directly to Qdrant point IDs
- citation payload fields stored with vectors
- indexing service
- retrieval service
- configurable Top-K and optional score threshold
- Qdrant connectivity helper
- local Qdrant Docker startup script and documentation
- fake/in-memory test infrastructure

Verification:

- 48 automated tests pass
- real Qdrant `v1.19.2` container successfully runs under Colima
- real application VectorStore successfully connected to Qdrant
- real collection creation, vector upsert, semantic search, payload retrieval, and score-threshold behavior verified
- temporary smoke-test collection was cleaned up
- no real OpenAI API call was made during milestone verification
- Qdrant compatibility warning was identified as belonging to the intentionally unreachable test and addressed only in that test with `check_compatibility=False`
- remaining third-party deprecation warnings were left unchanged
- Qdrant's Colima/virtiofs filesystem warning was reviewed and retained as a known development-environment limitation; no architecture change was made

Commit:

```text
19f7f43 feat: add embeddings and Qdrant vector layer
```

The Git working tree is clean and the commit is present on `origin/main`.

## Current Development Environment

The verified local Docker setup is:

- Docker CLI 29.2.1
- Colima as the working Docker runtime
- Docker context `colima`
- macOS Virtualization.Framework
- x86_64 architecture
- virtiofs mount type
- Docker Desktop not used
- Lima not used as the active runtime

Qdrant is intentionally a separate Docker container during development. The Python application is not yet containerized.

## Not Yet Implemented

- RAG engine / answer generation
- OpenAI GPT-5.4 mini answer generation
- real end-to-end OpenAI embedding/API integration
- chat API
- conversation API/UX beyond the database foundation
- React application
- Bootstrap UI
- authentication
- chat UI and streaming
- admin panel
- retrieval playground UI
- evaluation system
- application Dockerization / final Docker Compose topology
- CI
- deployment
- final portfolio README/content polish
- screenshots and final demo assets

## Intentionally Deferred

The following remain open and should not be silently finalized:

- exact supported document formats beyond PDF
- final chunk size and overlap values
- final retrieval Top-K
- final similarity threshold
- exact authentication implementation
- exact streaming mechanism
- production relational database
- application Docker Compose topology
- hosting/deployment provider
- evaluation methodology
- exact React architecture/visual design
- API route naming
- final admin metrics

# 48. Future Change-Control Procedure

If a future discussion proposes a significant change, use this procedure:

### Step 1

Explain:

- what is being proposed,
- why it may be useful,
- what existing decision it changes,
- consequences/tradeoffs.

### Step 2

Ask the user explicitly whether to approve the change.

### Step 3

Until approval:

- do not modify the canonical plan,
- do not treat the proposed change as an approved decision,
- do not implement an architecture-breaking change based solely on the proposal.

### Step 4

After explicit approval:

- update `MASTER_PLAN.md`,
- clearly move the affected item from proposal/open question to confirmed decision where appropriate,
- ensure the rest of the plan remains internally consistent.

---

# 49. Guiding Principle

The project should demonstrate **real understanding of RAG and modern AI engineering**, not merely demonstrate that an AI coding agent can generate a large amount of code.

The finished application should be:

> **Small enough to finish, sophisticated enough to impress, and simple enough to explain in an interview.**

---

# 50. Canonical Status

This document represents the **latest approved project plan as of 2026-10-11**. Milestones 0–4 have been implemented and reviewed; the next planned milestone is Milestone 5 — RAG engine.

Future implementation work should remain aligned with this document unless the user explicitly approves a change.

**End of MASTER_PLAN.md**
