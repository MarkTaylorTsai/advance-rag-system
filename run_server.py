#!/usr/bin/env python3
"""
Standalone RAG System Server

This script runs the RAG system as a standalone FastAPI server.
It uses the same setup as the test app but is configured for production use.

Usage:
    python run_server.py

Environment Variables:
    - RAG_EMBEDDING_ENGINE: ollama (default) | openai | azure_openai
    - RAG_EMBEDDING_MODEL: nomic-embed-text (default)
    - RAG_OLLAMA_BASE_URL: http://localhost:11434 (default)
    - DATABASE_URL: sqlite:///./rag_data/rag.db (default)
    - VECTOR_DB: chroma (default)
    - CHROMA_DATA_PATH: ./rag_data/chroma (default)
    - DATA_DIR: ./rag_data (default)
"""
import os
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import JSON

# Add project root to path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Set up rag_system module structure (same as test app)
import importlib
import types

if "rag_system" not in sys.modules:
    rag_system = types.ModuleType("rag_system")
    rag_system.__path__ = [str(ROOT)]
    sys.modules["rag_system"] = rag_system
    sys.modules["rag_system.backend"] = importlib.import_module("backend")

# Import RAG system components
from rag_system.backend.db import configure_db, get_scoped_session
from rag_system.backend.model_registry import register_model
from rag_system.backend.routers import knowledge, retrieval
from rag_system.backend.routers.retrieval import get_ef
from rag_system.backend.retrieval.utils import get_embedding_function
from rag_system.backend.settings import Settings

# Import minimal models (you'll need to provide your own User/File models)
# For now, we'll use simple stubs
from sqlalchemy import Column, String, BigInteger, Text
from sqlalchemy.orm import declarative_base
import time

Base = declarative_base()

# Minimal User model
class User(Base):
    __tablename__ = "user"
    id = Column(String, primary_key=True)
    role = Column(String, default="user")

# Minimal File model  
class File(Base):
    __tablename__ = "file"
    id = Column(String, primary_key=True)
    user_id = Column(String)
    filename = Column(Text)
    data = Column(JSON, default={})
    meta = Column(JSON, default={})
    hash = Column(String, nullable=True)
    created_at = Column(BigInteger, default=lambda: int(time.time()))
    updated_at = Column(BigInteger, default=lambda: int(time.time()))

# Minimal service stubs
class Users:
    @staticmethod
    def get_users_by_user_ids(user_ids, db):
        return db.query(User).filter(User.id.in_(user_ids)).all() if user_ids else []

class Files:
    @staticmethod
    def get_file_by_id(file_id, db):
        return db.query(File).filter(File.id == file_id).first()
    
    @staticmethod
    def get_file_by_id_and_user_id(file_id, user_id, db):
        return db.query(File).filter(File.id == file_id, File.user_id == user_id).first()
    
    @staticmethod
    def update_file_data_by_id(file_id, data, db):
        file = db.query(File).filter(File.id == file_id).first()
        if file:
            file.data = data
            file.updated_at = int(time.time())
            db.commit()
        return file
    
    @staticmethod
    def update_file_hash_by_id(file_id, file_hash, db):
        file = db.query(File).filter(File.id == file_id).first()
        if file:
            file.hash = file_hash
            file.updated_at = int(time.time())
            db.commit()
        return file
    
    @staticmethod
    def update_file_metadata_by_id(file_id, metadata, db):
        file = db.query(File).filter(File.id == file_id).first()
        if file:
            if file.meta is None:
                file.meta = {}
            file.meta.update(metadata)
            file.updated_at = int(time.time())
            db.commit()
        return file
    
    @staticmethod
    def delete_file_by_id(file_id, db):
        db.query(File).filter(File.id == file_id).delete()
        db.commit()

class Groups:
    @staticmethod
    def get_groups_by_member_id(user_id, db):
        return []

class Models:
    @staticmethod
    def get_all_models(db):
        return []
    
    @staticmethod
    def update_model_by_id(model_id, model_form, db):
        return None

class ModelForm:
    pass

class Storage:
    def get_file(self, file_path: str) -> str:
        return file_path
    
    def upload_file(self, file, filename: str, tags: dict):
        data_dir = os.getenv("DATA_DIR", "./rag_data")
        os.makedirs(data_dir, exist_ok=True)
        file_path = os.path.join(data_dir, filename)
        with open(file_path, "wb") as f:
            f.write(file)
        return file_path
    
    def delete_file(self, file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)

# Mock providers
class MockUserProvider:
    async def get_verified_user(self, request):
        return User(id="default-user", role="admin")
    
    async def get_admin_user(self, request):
        return User(id="default-user", role="admin")

class MockPermissionProvider:
    def has_access(self, user_id, access_type="write", access_control=None, user_group_ids=None, strict=True, db=None):
        return True
    
    def has_permission(self, user_id, permission_key, default_permissions, db=None):
        return True
    
    def get_users_with_access(self, access_type="write", access_control=None, db=None):
        return []

# Configure database
database_url = os.getenv("DATABASE_URL", "sqlite:///./rag_data/rag.db")
os.makedirs(os.path.dirname(database_url.replace("sqlite:///", "")), exist_ok=True)

configure_db(Base, JSON, get_scoped_session, get_scoped_session, get_scoped_session)

# Import RAG models to register them
import rag_system.backend.models.knowledge  # noqa: F401

# Register models
register_model("User", User)
register_model("Users", Users)
register_model("File", File)
register_model("Files", Files)
register_model("Groups", Groups)
register_model("Models", Models)
register_model("ModelForm", ModelForm)
register_model("Storage", Storage)

# Create FastAPI app
app = FastAPI(title="RAG System API", version="0.1.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(retrieval.router, prefix="/retrieval")
app.include_router(knowledge.router, prefix="/knowledge")

# Set default state values
app.state.YOUTUBE_LOADER_TRANSLATION = None

@app.on_event("startup")
async def startup():
    # Create database tables
    from sqlalchemy import create_engine
    engine = create_engine(database_url)
    Base.metadata.create_all(bind=engine)
    
    # Load configuration
    config = Settings()
    app.state.config = config
    
    # Set up providers
    app.state.rag_user_provider = MockUserProvider()
    app.state.rag_permission_provider = MockPermissionProvider()
    app.state.rag_get_session = get_scoped_session
    app.state.rag_storage_provider = Storage()
    
    # Initialize embedding function
    app.state.ef = get_ef(
        config.RAG_EMBEDDING_ENGINE,
        config.RAG_EMBEDDING_MODEL,
    )
    app.state.EMBEDDING_FUNCTION = get_embedding_function(
        config.RAG_EMBEDDING_ENGINE,
        config.RAG_EMBEDDING_MODEL,
        app.state.ef,
        config.RAG_OLLAMA_BASE_URL,
        config.RAG_OLLAMA_API_KEY,
        config.RAG_EMBEDDING_BATCH_SIZE,
        enable_async=config.ENABLE_ASYNC_EMBEDDING,
    )
    app.state.RERANKING_FUNCTION = None

@app.get("/")
async def root():
    return {
        "message": "RAG System API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/retrieval/config"
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting RAG System server on http://{host}:{port}")
    print(f"API docs available at http://{host}:{port}/docs")
    print(f"Make sure Ollama is running at {os.getenv('RAG_OLLAMA_BASE_URL', 'http://localhost:11434')}")
    
    uvicorn.run(app, host=host, port=port)

