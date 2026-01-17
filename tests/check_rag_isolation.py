import os
import sys
from contextlib import contextmanager

# Ensure the rag_system backend is on the path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
)


def test_isolation():
    print("--- Starting RAG Isolation Check ---")

    # 1. Verify core interfaces load
    try:
        from model_registry import register_model, get_model  # noqa: F401
        from storage import StorageProvider  # noqa: F401
        print("✅ Core RAG interfaces loaded.")
    except ImportError as exc:
        print(f"❌ Core loading failed: {exc}")
        return

    # 2. Check for leaks via sys.modules
    forbidden = "open_webui"
    leaked_modules = [m for m in sys.modules if m.startswith(forbidden)]
    if leaked_modules:
        print(
            f"❌ Dependency leak detected! The following modules were loaded: {leaked_modules}"
        )
    else:
        print("✅ No 'open_webui' modules found in sys.modules.")

    # 3. Test standalone DB configuration
    try:
        from db import configure_db

        class DummyBase:
            metadata = None

        class DummyJSONField:
            pass

        def dummy_get_db():
            return None

        @contextmanager
        def dummy_get_db_context(_db=None):
            yield None

        configure_db(DummyBase, DummyJSONField, dummy_get_db, dummy_get_db_context)
        print("✅ Database configured in isolation.")
    except Exception as exc:
        print(f"❌ Standalone DB config failed: {exc}")


if __name__ == "__main__":
    test_isolation()
