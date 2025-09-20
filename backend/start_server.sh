#!/bin/bash

# Activate virtual environment and start FastAPI server
cd "$(dirname "$0")"
source venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# ./backend/start_server.sh