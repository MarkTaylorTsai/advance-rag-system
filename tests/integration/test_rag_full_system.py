import time
import uuid

import pytest
from fastapi.testclient import TestClient

from tests.support.app import app
from tests.support.db import SessionLocal
from tests.support.models import File, User

@pytest.fixture(scope="session")
def client():
    # Set default state values that might be accessed before startup
    app.state.YOUTUBE_LOADER_TRANSLATION = None
    # Manually trigger startup event since TestClient doesn't do it automatically
    with TestClient(app) as test_client:
        # Trigger startup manually
        for handler in app.router.on_startup:
            handler()
        yield test_client


def _reset_db():
    from rag_system.backend.models.knowledge import Knowledge, KnowledgeFile

    db = SessionLocal()
    try:
        db.query(KnowledgeFile).delete()
        db.query(Knowledge).delete()
        db.query(File).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_state(client):
    _reset_db()
    client.post("/retrieval/reset/db")
    yield
    _reset_db()


def _ensure_user(user_id="test-user"):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id, role="admin", name="Test Admin")
            db.add(user)
            db.commit()
        return user
    finally:
        db.close()


def test_embedding_config_heartbeat(client):
    response = client.get("/retrieval/config")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] is True

    embed_response = client.get("/retrieval/embedding")
    assert embed_response.status_code == 200
    embed_payload = embed_response.json()
    assert embed_payload["RAG_EMBEDDING_ENGINE"] == "ollama"
    assert embed_payload["RAG_EMBEDDING_MODEL"]


def test_end_to_end_knowledge_query(client):
    _ensure_user()

    kb_response = client.post(
        "/knowledge/create",
        json={"name": "Test KB", "description": "Testing knowledge base"},
    )
    assert kb_response.status_code == 200
    kb_id = kb_response.json()["id"]

    process_response = client.post(
        "/retrieval/process/text",
        json={
            "name": "seed-text",
            "content": "The secret password is OpenWebUI-Rules.",
            "collection_name": kb_id,
        },
    )
    assert process_response.status_code == 200

    query_response = client.post(
        "/retrieval/query/collection",
        json={"collection_names": [kb_id], "query": "What is the secret password?"},
    )
    assert query_response.status_code == 200
    query_payload = query_response.json()
    assert "OpenWebUI-Rules" in " ".join(query_payload["documents"][0])


def test_file_processing_flow(client):
    _ensure_user()

    kb_response = client.post(
        "/knowledge/create",
        json={"name": "File KB", "description": "KB with file"},
    )
    assert kb_response.status_code == 200
    kb_id = kb_response.json()["id"]

    file_id = str(uuid.uuid4())
    now = int(time.time())
    db = SessionLocal()
    try:
        db.add(
            File(
                id=file_id,
                user_id="test-user",
                filename="sample.txt",
                data={"content": "File-based context for RAG testing."},
                meta={"content_type": "text/plain"},
                created_at=now,
                updated_at=now,
            )
        )
        db.commit()
    finally:
        db.close()

    add_response = client.post(
        f"/knowledge/{kb_id}/file/add", json={"file_id": file_id}
    )
    assert add_response.status_code == 200
    files_payload = add_response.json()["files"]
    assert any(file_row["id"] == file_id for file_row in files_payload)

    query_response = client.post(
        "/retrieval/query/collection",
        json={"collection_names": [kb_id], "query": "file-based context"},
    )
    assert query_response.status_code == 200
    query_payload = query_response.json()
    assert "File-based context" in " ".join(query_payload["documents"][0])
