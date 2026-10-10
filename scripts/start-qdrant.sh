#!/usr/bin/env bash
# Start (or restart) a local Qdrant container with persistent storage.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p qdrant_storage
docker rm -f company-knowledge-qdrant >/dev/null 2>&1 || true
docker run -d --name company-knowledge-qdrant \
  -p 6333:6333 \
  -v "$(pwd)/qdrant_storage:/qdrant/storage" \
  qdrant/qdrant:v1.19.2
echo "Qdrant running at http://localhost:6333 (dashboard: /dashboard)"
