rag_system
==========

Overview
--------
`rag_system` is a standalone Retrieval-Augmented Generation subsystem extracted from Open WebUI.
It is designed to be portable and embeddable in other FastAPI apps without importing `open_webui`
modules inside this directory.

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
