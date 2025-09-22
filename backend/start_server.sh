#!/bin/bash

# Activate virtual environment and start FastAPI server from repo root so package imports work
SCRIPT_DIR="$(dirname "$0")"
REPO_ROOT="${SCRIPT_DIR}/.."
cd "$REPO_ROOT"
source backend/venv/bin/activate
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# ./backend/start_server.sh