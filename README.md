rag_system
==========

Overview
--------
`rag_system` is a standalone Retrieval-Augmented Generation (RAG) backend you can embed into
any FastAPI app. It focuses on document ingestion, knowledge base management, embedding and
reranking, and fast retrieval across multiple vector stores and web sources.

What it enables
---------------
- Build searchable knowledge bases with access control and sharing rules.
- Ingest documents from files, URLs, web search, and external loaders.
- Configure and switch embedding / reranking providers (OpenAI, Ollama, Azure, external).
- Run hybrid search (semantic + BM25), metadata filters, and collection-level queries.
- Process batches of files and manage vector collections at scale.
- Expose clean API routes for retrieval, processing, and knowledge base operations.

Initialization
--------------
The host app must configure the RAG DB bindings and register models/providers at startup.

Minimal setup (Open WebUI example):
- Call `configure_db(...)` from `rag_system.backend.db`
- Register models via `register_model(...)` from `rag_system.backend.model_registry`
- Provide providers on `app.state`:
  - `rag_user_provider`
  - `rag_permission_provider`
  - `rag_get_session`
  - `rag_storage_provider`

Registry
--------
Required registrations (current usage):
- `User`, `UserModel`, `UserResponse`, `Users`
- `File`, `FileModel`, `FileMetadataResponse`, `FileUpdateForm`, `Files`
- `Groups`, `Chats`, `Notes`, `Models`, `ModelForm`
- `Storage`

Isolation Rule
--------------
No code inside `rag_system/` should import from `open_webui`.
Use providers and the model registry instead.

Checks
------
Run the isolation guardrail:
`make check-rag` (from `rag_system/`)

Config
------
See `rag_system/env.example` for environment variables used by the backend.

Post-migration smoke test
-------------------------
1) Creation flow:
   - Open the Knowledge workspace.
   - Create a new collection.
   - Confirms `KnowledgeAPI.createKnowledge` and model registry wiring.

2) Processing flow:
   - Upload a small PDF or text file to the collection.
   - Watch the status update.
   - Confirms storage provider + retrieval processing.

3) Inference flow:
   - Go to chat, tag the new collection, and ask a question.
   - Confirms scoped DB session + vector DB backend integration.
