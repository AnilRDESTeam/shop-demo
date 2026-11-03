#!/usr/bin/env bash
# First-time setup: venv, dependencies, Playwright browser.
set -e
cd "$(dirname "$0")/.."

if [ ! -x .venv/bin/python ]; then
  echo "Creating virtual environment (.venv) ..."
  python3 -m venv .venv
fi

echo "Installing dependencies ..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements-dev.txt

echo "Installing Chromium for browser tests ..."
if ! .venv/bin/python -m playwright install chromium; then
  echo "Chromium download blocked. Set SHOP_BROWSER_CHANNEL=msedge (or chrome) to use an installed browser instead."
fi

echo "Setup done. Next: scripts/run.sh"
