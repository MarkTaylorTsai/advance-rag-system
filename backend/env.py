import json
import logging
import os
from pathlib import Path

SRC_LOG_LEVELS = {}  # Legacy variable, keep for compatibility


GLOBAL_LOG_LEVEL = os.environ.get("GLOBAL_LOG_LEVEL", "").upper()
if GLOBAL_LOG_LEVEL in logging.getLevelNamesMapping():
    logging.basicConfig(level=GLOBAL_LOG_LEVEL, force=True)
else:
    GLOBAL_LOG_LEVEL = "INFO"

log = logging.getLogger(__name__)
log.info(f"GLOBAL_LOG_LEVEL: {GLOBAL_LOG_LEVEL}")

DOCKER = os.environ.get("DOCKER", "False").lower() == "true"

USE_CUDA = os.environ.get("USE_CUDA_DOCKER", "false")
if USE_CUDA.lower() == "true":
    try:
        import torch

        assert torch.cuda.is_available(), "CUDA not available"
        DEVICE_TYPE = "cuda"
    except Exception as e:
        cuda_error = (
            "Error when testing CUDA but USE_CUDA_DOCKER is true. "
            f"Resetting USE_CUDA_DOCKER to false: {e}"
        )
        os.environ["USE_CUDA_DOCKER"] = "false"
        USE_CUDA = "false"
        DEVICE_TYPE = "cpu"
else:
    DEVICE_TYPE = "cpu"

try:
    import torch

    if torch.backends.mps.is_available() and torch.backends.mps.is_built():
        DEVICE_TYPE = "mps"
except Exception:
    pass

SENTENCE_TRANSFORMERS_BACKEND = os.environ.get("SENTENCE_TRANSFORMERS_BACKEND", "")
SENTENCE_TRANSFORMERS_MODEL_KWARGS = os.environ.get(
    "SENTENCE_TRANSFORMERS_MODEL_KWARGS", "{}"
)
try:
    SENTENCE_TRANSFORMERS_MODEL_KWARGS = json.loads(SENTENCE_TRANSFORMERS_MODEL_KWARGS)
except Exception:
    SENTENCE_TRANSFORMERS_MODEL_KWARGS = {}

SENTENCE_TRANSFORMERS_CROSS_ENCODER_BACKEND = os.environ.get(
    "SENTENCE_TRANSFORMERS_CROSS_ENCODER_BACKEND", ""
)
SENTENCE_TRANSFORMERS_CROSS_ENCODER_MODEL_KWARGS = os.environ.get(
    "SENTENCE_TRANSFORMERS_CROSS_ENCODER_MODEL_KWARGS", "{}"
)
try:
    SENTENCE_TRANSFORMERS_CROSS_ENCODER_MODEL_KWARGS = json.loads(
        SENTENCE_TRANSFORMERS_CROSS_ENCODER_MODEL_KWARGS
    )
except Exception:
    SENTENCE_TRANSFORMERS_CROSS_ENCODER_MODEL_KWARGS = {}

SENTENCE_TRANSFORMERS_CROSS_ENCODER_SIGMOID_ACTIVATION_FUNCTION = os.environ.get(
    "SENTENCE_TRANSFORMERS_CROSS_ENCODER_SIGMOID_ACTIVATION_FUNCTION", ""
)

REQUESTS_VERIFY = os.environ.get("REQUESTS_VERIFY", "True").lower() == "true"
ENABLE_FORWARD_USER_INFO_HEADERS = (
    os.environ.get("ENABLE_FORWARD_USER_INFO_HEADERS", "False").lower() == "true"
)
OFFLINE_MODE = os.environ.get("OFFLINE_MODE", "False").lower() == "true"

AIOHTTP_CLIENT_TIMEOUT = os.environ.get("AIOHTTP_CLIENT_TIMEOUT", "")
try:
    AIOHTTP_CLIENT_TIMEOUT = float(AIOHTTP_CLIENT_TIMEOUT)
except ValueError:
    AIOHTTP_CLIENT_TIMEOUT = None

AIOHTTP_CLIENT_SESSION_SSL = os.environ.get("AIOHTTP_CLIENT_SESSION_SSL", "")
if AIOHTTP_CLIENT_SESSION_SSL != "":
    try:
        AIOHTTP_CLIENT_SESSION_SSL = bool(int(AIOHTTP_CLIENT_SESSION_SSL))
    except Exception:
        AIOHTTP_CLIENT_SESSION_SSL = None
else:
    AIOHTTP_CLIENT_SESSION_SSL = None

BASE_DIR = Path(__file__).resolve().parents[2]
BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = Path(os.getenv("DATA_DIR", BACKEND_DIR / "data")).resolve()
