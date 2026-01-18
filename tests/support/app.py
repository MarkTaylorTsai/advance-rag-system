import importlib
import os
import sys
import types
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import JSON

from tests.support.db import Base, SessionLocal, engine, get_db, get_db_context
from tests.support.models import (
    File,
    Files,
    Groups,
    ModelForm,
    Models,
    User,
    Users,
)

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

if "rag_system" not in sys.modules:
    rag_system = types.ModuleType("rag_system")
    rag_system.__path__ = [str(ROOT)]
    sys.modules["rag_system"] = rag_system
    sys.modules["rag_system.backend"] = importlib.import_module("backend")

from rag_system.backend.db import configure_db
from rag_system.backend.model_registry import register_model

# Configure DB BEFORE importing anything that depends on it
configure_db(Base, JSON, get_db, get_db_context, SessionLocal)

# Now safe to import RAG modules
from rag_system.backend.retrieval.utils import get_embedding_function


class TestUser:
    def __init__(self, user_id: str, role: str = "admin"):
        self.id = user_id
        self.role = role


class TestUserProvider:
    def __init__(self, user: TestUser):
        self._user = user

    async def get_verified_user(self, request):
        return self._user

    async def get_admin_user(self, request):
        return self._user


class AllowAllPermissionProvider:
    def has_access(
        self,
        user_id,
        access_type="write",
        access_control=None,
        user_group_ids=None,
        strict=True,
        db=None,
    ):
        return True

    def has_permission(
        self, user_id, permission_key, default_permissions, db=None
    ):
        return True

    def get_users_with_access(self, access_type="write", access_control=None, db=None):
        return []


class LocalStorageProvider:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def get_file(self, file_path: str) -> str:
        if os.path.isabs(file_path):
            return file_path
        return os.path.join(self.base_dir, file_path)

    def upload_file(self, file, filename: str, tags: dict):
        target = self.get_file(filename)
        with open(target, "wb") as f:
            f.write(file)
        return target

    def delete_all_files(self) -> None:
        for entry in os.listdir(self.base_dir):
            path = os.path.join(self.base_dir, entry)
            try:
                os.remove(path)
            except OSError:
                pass

    def delete_file(self, file_path: str) -> None:
        try:
            os.remove(self.get_file(file_path))
        except OSError:
            pass


class TestConfig:
    def __init__(self):
        self.BYPASS_ADMIN_ACCESS_CONTROL = True
        self.USER_PERMISSIONS = {}

        self.RAG_TEMPLATE = ""
        self.TOP_K = 5
        self.BYPASS_EMBEDDING_AND_RETRIEVAL = False
        self.RAG_FULL_CONTEXT = False
        self.ENABLE_RAG_HYBRID_SEARCH = False
        self.ENABLE_RAG_HYBRID_SEARCH_ENRICHED_TEXTS = False
        self.TOP_K_RERANKER = 5
        self.RELEVANCE_THRESHOLD = 0.0
        self.HYBRID_BM25_WEIGHT = 0.5

        self.CONTENT_EXTRACTION_ENGINE = ""
        self.PDF_EXTRACT_IMAGES = False

        self.RAG_EMBEDDING_ENGINE = os.getenv("RAG_EMBEDDING_ENGINE", "ollama")
        self.RAG_EMBEDDING_MODEL = os.getenv("RAG_EMBEDDING_MODEL", "nomic-embed-text")
        self.RAG_EMBEDDING_BATCH_SIZE = int(
            os.getenv("RAG_EMBEDDING_BATCH_SIZE", "16")
        )
        self.ENABLE_ASYNC_EMBEDDING = True

        self.RAG_OLLAMA_BASE_URL = os.getenv(
            "RAG_OLLAMA_BASE_URL", "http://ollama:11434"
        )
        self.RAG_OLLAMA_API_KEY = os.getenv("RAG_OLLAMA_API_KEY", "")
        self.RAG_OPENAI_API_BASE_URL = os.getenv("RAG_OPENAI_API_BASE_URL", "")
        self.RAG_OPENAI_API_KEY = os.getenv("RAG_OPENAI_API_KEY", "")
        self.RAG_AZURE_OPENAI_BASE_URL = os.getenv("RAG_AZURE_OPENAI_BASE_URL", "")
        self.RAG_AZURE_OPENAI_API_KEY = os.getenv("RAG_AZURE_OPENAI_API_KEY", "")
        self.RAG_AZURE_OPENAI_API_VERSION = os.getenv(
            "RAG_AZURE_OPENAI_API_VERSION", ""
        )

        self.RAG_RERANKING_MODEL = ""
        self.RAG_RERANKING_ENGINE = ""
        self.RAG_EXTERNAL_RERANKER_URL = ""
        self.RAG_EXTERNAL_RERANKER_API_KEY = ""
        self.RAG_EXTERNAL_RERANKER_TIMEOUT = ""

        self.TEXT_SPLITTER = ""
        self.ENABLE_MARKDOWN_HEADER_TEXT_SPLITTER = False
        self.CHUNK_SIZE = 500
        self.CHUNK_MIN_SIZE_TARGET = 200
        self.CHUNK_OVERLAP = 100

        self.FILE_MAX_SIZE = 0
        self.FILE_MAX_COUNT = 0
        self.FILE_IMAGE_COMPRESSION_WIDTH = 0
        self.FILE_IMAGE_COMPRESSION_HEIGHT = 0
        self.ALLOWED_FILE_EXTENSIONS = []

        self.ENABLE_GOOGLE_DRIVE_INTEGRATION = False
        self.ENABLE_ONEDRIVE_INTEGRATION = False

        self.ENABLE_WEB_SEARCH = False
        self.WEB_SEARCH_ENGINE = ""
        self.WEB_SEARCH_TRUST_ENV = False
        self.WEB_SEARCH_RESULT_COUNT = 3
        self.WEB_SEARCH_CONCURRENT_REQUESTS = 2
        self.WEB_LOADER_CONCURRENT_REQUESTS = 2
        self.WEB_SEARCH_DOMAIN_FILTER_LIST = []
        self.BYPASS_WEB_SEARCH_EMBEDDING_AND_RETRIEVAL = False
        self.BYPASS_WEB_SEARCH_WEB_LOADER = False
        self.OLLAMA_CLOUD_WEB_SEARCH_API_KEY = ""
        self.SEARXNG_QUERY_URL = ""
        self.SEARXNG_LANGUAGE = ""
        self.YACY_QUERY_URL = ""
        self.YACY_USERNAME = ""
        self.YACY_PASSWORD = ""
        self.GOOGLE_PSE_API_KEY = ""
        self.GOOGLE_PSE_ENGINE_ID = ""
        self.BRAVE_SEARCH_API_KEY = ""
        self.KAGI_SEARCH_API_KEY = ""
        self.MOJEEK_SEARCH_API_KEY = ""
        self.BOCHA_SEARCH_API_KEY = ""
        self.SERPSTACK_API_KEY = ""
        self.SERPSTACK_HTTPS = False
        self.SERPER_API_KEY = ""
        self.SERPLY_API_KEY = ""
        self.DDGS_BACKEND = ""
        self.TAVILY_API_KEY = ""
        self.SEARCHAPI_API_KEY = ""
        self.SEARCHAPI_ENGINE = ""
        self.SERPAPI_API_KEY = ""
        self.SERPAPI_ENGINE = ""
        self.JINA_API_KEY = ""
        self.JINA_API_BASE_URL = ""
        self.BING_SEARCH_V7_ENDPOINT = ""
        self.BING_SEARCH_V7_SUBSCRIPTION_KEY = ""
        self.EXA_API_KEY = ""
        self.PERPLEXITY_API_KEY = ""
        self.PERPLEXITY_MODEL = ""
        self.PERPLEXITY_SEARCH_CONTEXT_USAGE = ""
        self.PERPLEXITY_SEARCH_API_URL = ""
        self.SOUGOU_API_SID = ""
        self.SOUGOU_API_SK = ""
        self.WEB_LOADER_ENGINE = ""
        self.WEB_LOADER_TIMEOUT = 60
        self.ENABLE_WEB_LOADER_SSL_VERIFICATION = True
        self.PLAYWRIGHT_WS_URL = ""
        self.PLAYWRIGHT_TIMEOUT = 60
        self.FIRECRAWL_API_KEY = ""
        self.FIRECRAWL_API_BASE_URL = ""
        self.EXTERNAL_WEB_SEARCH_URL = ""
        self.EXTERNAL_WEB_SEARCH_API_KEY = ""
        self.EXTERNAL_DOCUMENT_LOADER_URL = ""
        self.EXTERNAL_DOCUMENT_LOADER_API_KEY = ""
        self.TIKA_SERVER_URL = ""
        self.DOCLING_SERVER_URL = ""
        self.DOCLING_API_KEY = ""
        self.DOCLING_PARAMS = {}
        self.DOCUMENT_INTELLIGENCE_ENDPOINT = ""
        self.DOCUMENT_INTELLIGENCE_KEY = ""
        self.DOCUMENT_INTELLIGENCE_MODEL = ""
        self.MISTRAL_OCR_API_BASE_URL = ""
        self.MISTRAL_OCR_API_KEY = ""
        self.MINERU_API_MODE = ""
        self.MINERU_API_URL = ""
        self.MINERU_API_KEY = ""
        self.MINERU_API_TIMEOUT = ""
        self.MINERU_PARAMS = {}
        self.DATALAB_MARKER_API_KEY = ""
        self.DATALAB_MARKER_API_BASE_URL = ""
        self.DATALAB_MARKER_ADDITIONAL_CONFIG = {}
        self.DATALAB_MARKER_SKIP_CACHE = False
        self.DATALAB_MARKER_FORCE_OCR = False
        self.DATALAB_MARKER_PAGINATE = False
        self.DATALAB_MARKER_STRIP_EXISTING_OCR = False
        self.DATALAB_MARKER_DISABLE_IMAGE_EXTRACTION = False
        self.DATALAB_MARKER_FORMAT_LINES = False
        self.DATALAB_MARKER_USE_LLM = False
        self.DATALAB_MARKER_OUTPUT_FORMAT = ""
        self.EXTERNAL_DOCUMENT_LOADER_TIMEOUT = 60

    def __getattr__(self, name):
        return None


def _get_session_provider():
    def _session():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    return _session


# Ensure RAG SQLAlchemy models are registered on the shared Base
import rag_system.backend.models.knowledge  # noqa: F401

from rag_system.backend.routers import knowledge, retrieval
from rag_system.backend.routers.retrieval import get_ef


app = FastAPI()

register_model("User", User)
register_model("Users", Users)
register_model("File", File)
register_model("Files", Files)
register_model("Groups", Groups)
register_model("Models", Models)
register_model("ModelForm", ModelForm)

app.include_router(retrieval.router, prefix="/retrieval")
app.include_router(knowledge.router, prefix="/knowledge")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

    config = TestConfig()
    app.state.config = config

    test_user = TestUser(user_id="test-user", role="admin")
    app.state.rag_user_provider = TestUserProvider(test_user)
    app.state.rag_permission_provider = AllowAllPermissionProvider()
    app.state.rag_get_session = _get_session_provider()
    app.state.rag_storage_provider = LocalStorageProvider(
        os.getenv("RAG_TEST_UPLOAD_DIR", "/tmp/rag_test_uploads")
    )

    app.state.ef = get_ef(
        config.RAG_EMBEDDING_ENGINE, config.RAG_EMBEDDING_MODEL
    )
    app.state.EMBEDDING_FUNCTION = get_embedding_function(
        config.RAG_EMBEDDING_ENGINE,
        config.RAG_EMBEDDING_MODEL,
        app.state.ef,
        (
            config.RAG_OPENAI_API_BASE_URL
            if config.RAG_EMBEDDING_ENGINE == "openai"
            else config.RAG_OLLAMA_BASE_URL
            if config.RAG_EMBEDDING_ENGINE == "ollama"
            else config.RAG_AZURE_OPENAI_BASE_URL
        ),
        (
            config.RAG_OPENAI_API_KEY
            if config.RAG_EMBEDDING_ENGINE == "openai"
            else config.RAG_OLLAMA_API_KEY
            if config.RAG_EMBEDDING_ENGINE == "ollama"
            else config.RAG_AZURE_OPENAI_API_KEY
        ),
        config.RAG_EMBEDDING_BATCH_SIZE,
        azure_api_version=(
            config.RAG_AZURE_OPENAI_API_VERSION
            if config.RAG_EMBEDDING_ENGINE == "azure_openai"
            else None
        ),
        enable_async=config.ENABLE_ASYNC_EMBEDDING,
    )
    app.state.RERANKING_FUNCTION = None
    app.state.YOUTUBE_LOADER_TRANSLATION = None