#!/usr/bin/env bash
# Start the shop on 127.0.0.1 (local only). Set PORT to change the port.
cd "$(dirname "$0")/.."

PORT="${PORT:-8080}"
echo "Open http://localhost:$PORT"
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port "$PORT" --reload
