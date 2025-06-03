#!/bin/bash
echo "Starting Translate Export Agent..."
echo "API: http://localhost:8000"
echo "UI: http://localhost:8501"

# Start API server
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &

# Wait a bit for API to start
sleep 2

# Start Streamlit UI
streamlit run streamlit_ui.py
