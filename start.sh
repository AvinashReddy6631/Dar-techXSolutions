#!/bin/bash

# Activate virtual environment if exists
echo "Starting Dar-techXSolutions FastAPI App..."

if [ -d "venv" ]; then
  source venv/bin/activate
  echo "✔ Virtual environment activated"
fi

# Install requirements (optional safety)
pip install -r requirements.txt

# Run app with uvicorn
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
