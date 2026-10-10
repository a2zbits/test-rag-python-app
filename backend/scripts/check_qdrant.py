"""Check Qdrant connectivity: `uv run python -m scripts.check_qdrant`."""

import sys

from app.core.config import get_settings
from app.services.vector_store import VectorStore

if __name__ == "__main__":
    settings = get_settings()
    ok = VectorStore().is_healthy()
    print(f"Qdrant at {settings.qdrant_url}: {'reachable' if ok else 'NOT reachable'}")
    sys.exit(0 if ok else 1)
