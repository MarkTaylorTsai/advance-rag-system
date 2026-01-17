import os
from pathlib import Path

from rag_system.backend.env import DATA_DIR

ENV = os.environ.get("ENV", "dev")
DEFAULT_LOCALE = os.environ.get("DEFAULT_LOCALE", "")

DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DATA_DIR}/webui.db")
if "postgres://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

UPLOAD_DIR = Path(DATA_DIR) / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

WEB_LOADER_ENGINE = os.environ.get("WEB_LOADER_ENGINE", "")
WEB_LOADER_TIMEOUT = int(os.environ.get("WEB_LOADER_TIMEOUT", "60"))
WEB_FETCH_FILTER_LIST = [
    entry.strip()
    for entry in os.environ.get("WEB_FETCH_FILTER_LIST", "").split(",")
    if entry.strip()
]
ENABLE_RAG_LOCAL_WEB_FETCH = (
    os.getenv("ENABLE_RAG_LOCAL_WEB_FETCH", "False").lower() == "true"
)

EXTERNAL_WEB_LOADER_URL = os.environ.get("EXTERNAL_WEB_LOADER_URL", "")
EXTERNAL_WEB_LOADER_API_KEY = os.environ.get("EXTERNAL_WEB_LOADER_API_KEY", "")

PLAYWRIGHT_WS_URL = os.environ.get("PLAYWRIGHT_WS_URL", "")
PLAYWRIGHT_TIMEOUT = int(os.environ.get("PLAYWRIGHT_TIMEOUT", "60"))

FIRECRAWL_API_BASE_URL = os.environ.get("FIRECRAWL_API_BASE_URL", "")
FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
FIRECRAWL_TIMEOUT = int(os.environ.get("FIRECRAWL_TIMEOUT", "60"))

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
TAVILY_EXTRACT_DEPTH = int(os.environ.get("TAVILY_EXTRACT_DEPTH", "3"))

RAG_EMBEDDING_QUERY_PREFIX = os.environ.get("RAG_EMBEDDING_QUERY_PREFIX", None)
RAG_EMBEDDING_CONTENT_PREFIX = os.environ.get("RAG_EMBEDDING_CONTENT_PREFIX", None)
RAG_EMBEDDING_PREFIX_FIELD_NAME = os.environ.get("RAG_EMBEDDING_PREFIX_FIELD_NAME", None)

RAG_EMBEDDING_MODEL_AUTO_UPDATE = (
    ENV == "prod"
    and os.environ.get("RAG_EMBEDDING_MODEL_AUTO_UPDATE", "True").lower() == "true"
)
RAG_EMBEDDING_MODEL_TRUST_REMOTE_CODE = (
    os.environ.get("RAG_EMBEDDING_MODEL_TRUST_REMOTE_CODE", "True").lower() == "true"
)
RAG_RERANKING_MODEL_AUTO_UPDATE = (
    ENV == "prod"
    and os.environ.get("RAG_RERANKING_MODEL_AUTO_UPDATE", "True").lower() == "true"
)
RAG_RERANKING_MODEL_TRUST_REMOTE_CODE = (
    os.environ.get("RAG_RERANKING_MODEL_TRUST_REMOTE_CODE", "True").lower() == "true"
)

VECTOR_DB = os.environ.get("VECTOR_DB", "chroma")

# Chroma
CHROMA_DATA_PATH = f"{DATA_DIR}/vector_db"
CHROMA_TENANT = os.environ.get("CHROMA_TENANT", "default_tenant")
CHROMA_DATABASE = os.environ.get("CHROMA_DATABASE", "default_database")
CHROMA_HTTP_HOST = os.environ.get("CHROMA_HTTP_HOST", "")
CHROMA_HTTP_PORT = int(os.environ.get("CHROMA_HTTP_PORT", "8000"))
CHROMA_CLIENT_AUTH_PROVIDER = os.environ.get("CHROMA_CLIENT_AUTH_PROVIDER", "")
CHROMA_CLIENT_AUTH_CREDENTIALS = os.environ.get("CHROMA_CLIENT_AUTH_CREDENTIALS", "")
CHROMA_HTTP_HEADERS = os.environ.get("CHROMA_HTTP_HEADERS", "")
if CHROMA_HTTP_HEADERS:
    CHROMA_HTTP_HEADERS = dict([pair.split("=") for pair in CHROMA_HTTP_HEADERS.split(",")])
else:
    CHROMA_HTTP_HEADERS = None
CHROMA_HTTP_SSL = os.environ.get("CHROMA_HTTP_SSL", "false").lower() == "true"

# Milvus
MILVUS_URI = os.environ.get("MILVUS_URI", f"{DATA_DIR}/vector_db/milvus.db")
MILVUS_DB = os.environ.get("MILVUS_DB", "default")
MILVUS_TOKEN = os.environ.get("MILVUS_TOKEN", None)
MILVUS_INDEX_TYPE = os.environ.get("MILVUS_INDEX_TYPE", "HNSW")
MILVUS_METRIC_TYPE = os.environ.get("MILVUS_METRIC_TYPE", "COSINE")
MILVUS_HNSW_M = int(os.environ.get("MILVUS_HNSW_M", "16"))
MILVUS_HNSW_EFCONSTRUCTION = int(os.environ.get("MILVUS_HNSW_EFCONSTRUCTION", "100"))
MILVUS_IVF_FLAT_NLIST = int(os.environ.get("MILVUS_IVF_FLAT_NLIST", "128"))
MILVUS_DISKANN_MAX_DEGREE = int(os.environ.get("MILVUS_DISKANN_MAX_DEGREE", "56"))
MILVUS_DISKANN_SEARCH_LIST_SIZE = int(
    os.environ.get("MILVUS_DISKANN_SEARCH_LIST_SIZE", "100")
)
ENABLE_MILVUS_MULTITENANCY_MODE = (
    os.environ.get("ENABLE_MILVUS_MULTITENANCY_MODE", "false").lower() == "true"
)
MILVUS_COLLECTION_PREFIX = os.environ.get("MILVUS_COLLECTION_PREFIX", "open_webui")

# Qdrant
QDRANT_URI = os.environ.get("QDRANT_URI", None)
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY", None)
QDRANT_ON_DISK = os.environ.get("QDRANT_ON_DISK", "false").lower() == "true"
QDRANT_PREFER_GRPC = os.environ.get("QDRANT_PREFER_GRPC", "false").lower() == "true"
QDRANT_GRPC_PORT = int(os.environ.get("QDRANT_GRPC_PORT", "6334"))
QDRANT_TIMEOUT = int(os.environ.get("QDRANT_TIMEOUT", "5"))
QDRANT_HNSW_M = int(os.environ.get("QDRANT_HNSW_M", "16"))
ENABLE_QDRANT_MULTITENANCY_MODE = (
    os.environ.get("ENABLE_QDRANT_MULTITENANCY_MODE", "true").lower() == "true"
)
QDRANT_COLLECTION_PREFIX = os.environ.get("QDRANT_COLLECTION_PREFIX", "open-webui")

# Weaviate
WEAVIATE_HTTP_HOST = os.environ.get("WEAVIATE_HTTP_HOST", "")
WEAVIATE_HTTP_PORT = int(os.environ.get("WEAVIATE_HTTP_PORT", "8080"))
WEAVIATE_GRPC_PORT = int(os.environ.get("WEAVIATE_GRPC_PORT", "50051"))
WEAVIATE_API_KEY = os.environ.get("WEAVIATE_API_KEY")

# OpenSearch
OPENSEARCH_URI = os.environ.get("OPENSEARCH_URI", "https://localhost:9200")
OPENSEARCH_SSL = os.environ.get("OPENSEARCH_SSL", "true").lower() == "true"
OPENSEARCH_CERT_VERIFY = os.environ.get("OPENSEARCH_CERT_VERIFY", "false").lower() == "true"
OPENSEARCH_USERNAME = os.environ.get("OPENSEARCH_USERNAME", None)
OPENSEARCH_PASSWORD = os.environ.get("OPENSEARCH_PASSWORD", None)

# ElasticSearch
ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "https://localhost:9200")
ELASTICSEARCH_CA_CERTS = os.environ.get("ELASTICSEARCH_CA_CERTS", None)
ELASTICSEARCH_API_KEY = os.environ.get("ELASTICSEARCH_API_KEY", None)
ELASTICSEARCH_USERNAME = os.environ.get("ELASTICSEARCH_USERNAME", None)
ELASTICSEARCH_PASSWORD = os.environ.get("ELASTICSEARCH_PASSWORD", None)
ELASTICSEARCH_CLOUD_ID = os.environ.get("ELASTICSEARCH_CLOUD_ID", None)
SSL_ASSERT_FINGERPRINT = os.environ.get("SSL_ASSERT_FINGERPRINT", None)
ELASTICSEARCH_INDEX_PREFIX = os.environ.get(
    "ELASTICSEARCH_INDEX_PREFIX", "open_webui_collections"
)

# Pgvector
PGVECTOR_DB_URL = os.environ.get("PGVECTOR_DB_URL", DATABASE_URL)
PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH = int(
    os.environ.get("PGVECTOR_INITIALIZE_MAX_VECTOR_LENGTH", "1536")
)
PGVECTOR_USE_HALFVEC = os.getenv("PGVECTOR_USE_HALFVEC", "false").lower() == "true"
PGVECTOR_CREATE_EXTENSION = os.getenv("PGVECTOR_CREATE_EXTENSION", "true").lower() == "true"
PGVECTOR_PGCRYPTO = os.getenv("PGVECTOR_PGCRYPTO", "false").lower() == "true"
PGVECTOR_PGCRYPTO_KEY = os.getenv("PGVECTOR_PGCRYPTO_KEY", None)

PGVECTOR_POOL_SIZE = os.environ.get("PGVECTOR_POOL_SIZE", None)
if PGVECTOR_POOL_SIZE is not None:
    try:
        PGVECTOR_POOL_SIZE = int(PGVECTOR_POOL_SIZE)
    except Exception:
        PGVECTOR_POOL_SIZE = None

PGVECTOR_POOL_MAX_OVERFLOW = os.environ.get("PGVECTOR_POOL_MAX_OVERFLOW", 0)
if PGVECTOR_POOL_MAX_OVERFLOW == "":
    PGVECTOR_POOL_MAX_OVERFLOW = 0
else:
    try:
        PGVECTOR_POOL_MAX_OVERFLOW = int(PGVECTOR_POOL_MAX_OVERFLOW)
    except Exception:
        PGVECTOR_POOL_MAX_OVERFLOW = 0

PGVECTOR_POOL_TIMEOUT = os.environ.get("PGVECTOR_POOL_TIMEOUT", 30)
if PGVECTOR_POOL_TIMEOUT == "":
    PGVECTOR_POOL_TIMEOUT = 30
else:
    try:
        PGVECTOR_POOL_TIMEOUT = int(PGVECTOR_POOL_TIMEOUT)
    except Exception:
        PGVECTOR_POOL_TIMEOUT = 30

PGVECTOR_POOL_RECYCLE = os.environ.get("PGVECTOR_POOL_RECYCLE", 3600)
if PGVECTOR_POOL_RECYCLE == "":
    PGVECTOR_POOL_RECYCLE = 3600
else:
    try:
        PGVECTOR_POOL_RECYCLE = int(PGVECTOR_POOL_RECYCLE)
    except Exception:
        PGVECTOR_POOL_RECYCLE = 3600

PGVECTOR_INDEX_METHOD = os.getenv("PGVECTOR_INDEX_METHOD", "").strip().lower()
if PGVECTOR_INDEX_METHOD not in ("ivfflat", "hnsw", ""):
    PGVECTOR_INDEX_METHOD = ""

PGVECTOR_HNSW_M = os.environ.get("PGVECTOR_HNSW_M", 16)
if PGVECTOR_HNSW_M == "":
    PGVECTOR_HNSW_M = 16
else:
    try:
        PGVECTOR_HNSW_M = int(PGVECTOR_HNSW_M)
    except Exception:
        PGVECTOR_HNSW_M = 16

PGVECTOR_HNSW_EF_CONSTRUCTION = os.environ.get("PGVECTOR_HNSW_EF_CONSTRUCTION", 64)
if PGVECTOR_HNSW_EF_CONSTRUCTION == "":
    PGVECTOR_HNSW_EF_CONSTRUCTION = 64
else:
    try:
        PGVECTOR_HNSW_EF_CONSTRUCTION = int(PGVECTOR_HNSW_EF_CONSTRUCTION)
    except Exception:
        PGVECTOR_HNSW_EF_CONSTRUCTION = 64

PGVECTOR_IVFFLAT_LISTS = os.environ.get("PGVECTOR_IVFFLAT_LISTS", 100)
if PGVECTOR_IVFFLAT_LISTS == "":
    PGVECTOR_IVFFLAT_LISTS = 100
else:
    try:
        PGVECTOR_IVFFLAT_LISTS = int(PGVECTOR_IVFFLAT_LISTS)
    except Exception:
        PGVECTOR_IVFFLAT_LISTS = 100

# OpenGauss
OPENGAUSS_DB_URL = os.environ.get("OPENGAUSS_DB_URL", "")
OPENGAUSS_INITIALIZE_MAX_VECTOR_LENGTH = int(
    os.environ.get("OPENGAUSS_INITIALIZE_MAX_VECTOR_LENGTH", "1536")
)
OPENGAUSS_POOL_SIZE = os.environ.get("OPENGAUSS_POOL_SIZE", None)
if OPENGAUSS_POOL_SIZE is not None:
    try:
        OPENGAUSS_POOL_SIZE = int(OPENGAUSS_POOL_SIZE)
    except Exception:
        OPENGAUSS_POOL_SIZE = None
OPENGAUSS_POOL_MAX_OVERFLOW = os.environ.get("OPENGAUSS_POOL_MAX_OVERFLOW", 0)
if OPENGAUSS_POOL_MAX_OVERFLOW == "":
    OPENGAUSS_POOL_MAX_OVERFLOW = 0
else:
    try:
        OPENGAUSS_POOL_MAX_OVERFLOW = int(OPENGAUSS_POOL_MAX_OVERFLOW)
    except Exception:
        OPENGAUSS_POOL_MAX_OVERFLOW = 0
OPENGAUSS_POOL_TIMEOUT = os.environ.get("OPENGAUSS_POOL_TIMEOUT", 30)
if OPENGAUSS_POOL_TIMEOUT == "":
    OPENGAUSS_POOL_TIMEOUT = 30
else:
    try:
        OPENGAUSS_POOL_TIMEOUT = int(OPENGAUSS_POOL_TIMEOUT)
    except Exception:
        OPENGAUSS_POOL_TIMEOUT = 30
OPENGAUSS_POOL_RECYCLE = os.environ.get("OPENGAUSS_POOL_RECYCLE", 3600)
if OPENGAUSS_POOL_RECYCLE == "":
    OPENGAUSS_POOL_RECYCLE = 3600
else:
    try:
        OPENGAUSS_POOL_RECYCLE = int(OPENGAUSS_POOL_RECYCLE)
    except Exception:
        OPENGAUSS_POOL_RECYCLE = 3600

# Oracle 23ai
ORACLE_DB_USER = os.environ.get("ORACLE_DB_USER", "")
ORACLE_DB_PASSWORD = os.environ.get("ORACLE_DB_PASSWORD", "")
ORACLE_DB_DSN = os.environ.get("ORACLE_DB_DSN", "")
ORACLE_DB_POOL_MIN = int(os.environ.get("ORACLE_DB_POOL_MIN", "1"))
ORACLE_DB_POOL_MAX = int(os.environ.get("ORACLE_DB_POOL_MAX", "5"))
ORACLE_DB_POOL_INCREMENT = int(os.environ.get("ORACLE_DB_POOL_INCREMENT", "1"))
ORACLE_DB_USE_WALLET = os.environ.get("ORACLE_DB_USE_WALLET", "false").lower() == "true"
ORACLE_WALLET_DIR = os.environ.get("ORACLE_WALLET_DIR", "")
ORACLE_WALLET_PASSWORD = os.environ.get("ORACLE_WALLET_PASSWORD", "")
ORACLE_VECTOR_LENGTH = int(os.environ.get("ORACLE_VECTOR_LENGTH", "1536"))

# Pinecone
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
PINECONE_ENVIRONMENT = os.environ.get("PINECONE_ENVIRONMENT", "")
PINECONE_CLOUD = os.environ.get("PINECONE_CLOUD", "")
PINECONE_INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "")
PINECONE_METRIC = os.environ.get("PINECONE_METRIC", "cosine")
PINECONE_DIMENSION = int(os.environ.get("PINECONE_DIMENSION", "1536"))

# S3Vector
S3_VECTOR_BUCKET_NAME = os.environ.get("S3_VECTOR_BUCKET_NAME", "")
S3_VECTOR_REGION = os.environ.get("S3_VECTOR_REGION", "")

# External web search engines
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
FIRECRAWL_API_BASE_URL = os.environ.get("FIRECRAWL_API_BASE_URL", "")
FIRECRAWL_API_KEY = os.environ.get("FIRECRAWL_API_KEY", "")
FIRECRAWL_TIMEOUT = int(os.environ.get("FIRECRAWL_TIMEOUT", "60"))
