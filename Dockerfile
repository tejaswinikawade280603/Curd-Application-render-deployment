# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Convert line endings and make start script executable
RUN apt-get update && apt-get install -y dos2unix && \
    dos2unix start.sh && \
    chmod +x start.sh && \
    apt-get remove -y dos2unix && \
    rm -rf /var/lib/apt/lists/*

# Expose port (Railway will set PORT env variable)
EXPOSE ${PORT:-5000}

# Set environment variables
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Use start.sh script that handles migrations and seeding
CMD ["./start.sh"]
