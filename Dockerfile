FROM python:3.10-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY test_app.py .
EXPOSE 8000
cat > Dockerfile << 'EOF'
FROM python:3.10-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY test_app.py .
EXPOSE 8000
CMD ["uvicorn", "test_app:app", "--host", "0.0.0.0", "--port", "8000"]
