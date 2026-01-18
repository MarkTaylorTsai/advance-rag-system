# Quick Start Guide

## Fixes Applied ✅

1. **Makefile** - Fixed to use `docker-compose` (your system's version)
2. **Virtual Environment** - Added setup script to avoid system-wide installs
3. **Python Command** - Updated docs to use `python3`

## Setup (One-Time)

```bash
# Run the setup script (creates venv and installs dependencies)
./setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -e ./backend uvicorn
```

## Running Tests

```bash
# Make sure Ollama is running with nomic-embed-text model
ollama serve  # In another terminal
ollama pull nomic-embed-text  # If needed

# Run integration tests
make test-integration
```

## Running the Server

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Make sure Ollama is running
ollama serve  # In another terminal

# Run the server
python3 run_server.py
```

The server will start on `http://localhost:8000`

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/retrieval/config

## Common Issues

**"python: command not found"**
- Use `python3` instead of `python`

**"externally-managed-environment"**
- Use a virtual environment: `python3 -m venv venv && source venv/bin/activate`

**"docker compose: unknown flag"**
- Your system uses `docker-compose` (standalone), which is now handled correctly

**Tests fail**
- Ensure Ollama is running: `ollama list` should show `nomic-embed-text`
- Check `RAG_OLLAMA_BASE_URL` environment variable

