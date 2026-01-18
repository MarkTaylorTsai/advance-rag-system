# Running the RAG System

## System Status ✅

**The system is functioning well!** All integration tests pass:
- ✅ `test_embedding_config_heartbeat` - Configuration and embedding endpoints work
- ✅ `test_end_to_end_knowledge_query` - Full knowledge base creation and query flow
- ✅ `test_file_processing_flow` - File upload and processing works

## Tests: Keep Them! 📦

**DO NOT delete the tests** - they are valuable for:
- Ensuring the system works after changes
- Verifying integration with external services (Ollama)
- Catching regressions
- Documenting expected behavior

The tests are in `tests/integration/` and can be run with:
```bash
make test-integration
```

## Running the System

### Option 1: Standalone Server (Recommended for Testing)

A standalone server script is provided: `run_server.py`

**Prerequisites:**
1. Ollama running with `nomic-embed-text` model:
   ```bash
   ollama serve  # In one terminal
   ollama pull nomic-embed-text  # If not already installed
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ./backend uvicorn
   ```

3. Run the server:
   ```bash
   python3 run_server.py
   # Or if venv is activated:
   python run_server.py
   ```

The server will start on `http://localhost:8000` with:
- API docs at `http://localhost:8000/docs`
- Health check at `http://localhost:8000/retrieval/config`

**Environment Variables:**
```bash
export RAG_EMBEDDING_ENGINE=ollama
export RAG_EMBEDDING_MODEL=nomic-embed-text
export RAG_OLLAMA_BASE_URL=http://localhost:11434
export DATABASE_URL=sqlite:///./rag_data/rag.db
export VECTOR_DB=chroma
export CHROMA_DATA_PATH=./rag_data/chroma
export DATA_DIR=./rag_data
```

### Option 2: Integration with Your FastAPI App

The RAG system is designed to be embedded into an existing FastAPI application. See `tests/support/app.py` for a complete example of how to:

1. Configure the database
2. Register models
3. Set up providers (user, permission, storage)
4. Include the routers

Key steps:
```python
from rag_system.backend.db import configure_db
from rag_system.backend.model_registry import register_model
from rag_system.backend.routers import knowledge, retrieval

# Configure DB
configure_db(Base, JSON, get_db, get_db_context, SessionLocal)

# Register your models
register_model("User", YourUserModel)
register_model("Files", YourFilesService)
# ... etc

# Include routers
app.include_router(retrieval.router, prefix="/retrieval")
app.include_router(knowledge.router, prefix="/knowledge")

# Set up providers in startup
app.state.rag_user_provider = YourUserProvider()
app.state.rag_permission_provider = YourPermissionProvider()
app.state.rag_get_session = your_get_session_function
app.state.rag_storage_provider = YourStorageProvider()
```

## Frontend Integration

The `frontend/` directory contains **Svelte components** designed to be integrated into Open WebUI or another Svelte-based application. These are not a standalone frontend.

**To use with Open WebUI:**
1. The components are already structured for Open WebUI integration
2. Import them in your Open WebUI frontend
3. The API endpoints (`/retrieval/*` and `/knowledge/*`) are already compatible

**To create a custom frontend:**
1. Use the API endpoints documented at `/docs` when running the server
2. Key endpoints:
   - `GET /retrieval/config` - Get configuration
   - `GET /retrieval/embedding` - Get embedding settings
   - `POST /knowledge/create` - Create knowledge base
   - `POST /retrieval/process/text` - Process text content
   - `POST /retrieval/query/collection` - Query knowledge base
   - `GET /knowledge/{id}/files` - List files in knowledge base

**Example frontend integration:**
```javascript
// Create a knowledge base
const response = await fetch('http://localhost:8000/knowledge/create', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'My Knowledge Base',
    description: 'Test KB'
  })
});

// Process text
await fetch('http://localhost:8000/retrieval/process/text', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'document.txt',
    content: 'Your content here',
    collection_name: kbId
  })
});

// Query
const queryResponse = await fetch('http://localhost:8000/retrieval/query/collection', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    collection_names: [kbId],
    query: 'Your question'
  })
});
```

## Quick Start Checklist

- [ ] Ollama is running with `nomic-embed-text` model
- [ ] Virtual environment created and activated
- [ ] Dependencies installed: `pip install -e ./backend uvicorn`
- [ ] Environment variables set (or using defaults)
- [ ] Run `python3 run_server.py`
- [ ] Visit `http://localhost:8000/docs` to explore the API
- [ ] Test with: `curl http://localhost:8000/retrieval/config`

## Troubleshooting

**Tests fail:**
- Ensure Ollama is running: `ollama list` should show `nomic-embed-text`
- Check `RAG_OLLAMA_BASE_URL` is correct

**Server won't start:**
- Check all dependencies are installed (use virtual environment)
- Verify database path is writable
- Ensure Ollama is accessible
- Use `python3` instead of `python` if `python` command not found

**Embedding errors:**
- Verify Ollama model is loaded: `ollama list`
- Check `RAG_OLLAMA_BASE_URL` points to your Ollama instance

