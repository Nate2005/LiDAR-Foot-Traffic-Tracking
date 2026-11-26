#!/usr/bin/env bash
# Set up and start the backend (Linux). Run from anywhere.
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate

pip install -q --upgrade pip
pip install -q --group dev

if [ ! -f data/campus_traffic.db ]; then
    python scripts/create_db.py
fi

exec uvicorn api.main:app --app-dir src
