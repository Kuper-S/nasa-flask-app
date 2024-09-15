# Base image with a specific version of Debian for security
FROM python:3.9-slim-bullseye

# Set labels and non-root user
LABEL maintainer="Super-Kuper" version="1.0.0"
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install system dependencies and upgrade system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install dependencies (including gunicorn)
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Set permissions for the application directory
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Command to run Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
