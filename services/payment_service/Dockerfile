FROM python:3.9-slim

WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn redis

# Run service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]