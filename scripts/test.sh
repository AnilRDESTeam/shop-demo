#!/usr/bin/env bash
# Run unit + API tests.
cd "$(dirname "$0")/.."

.venv/bin/python -m pytest
