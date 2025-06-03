FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000 8501

# Create startup script
RUN echo '#!/bin/bash' > /app/start.sh && \
    echo 'uvicorn src.api.main:app --host 0.0.0.0 --port 8000 &' >> /app/start.sh && \
    echo 'streamlit run streamlit_ui.py --server.port 8501 --server.address 0.0.0.0' >> /app/start.sh && \
    chmod +x /app/start.sh

CMD ["/app/start.sh"]
