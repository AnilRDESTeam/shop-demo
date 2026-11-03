#!/usr/bin/env bash
# Run browser tests (starts its own server on port 8099).
cd "$(dirname "$0")/.."

.venv/bin/python -m pytest -m e2e
