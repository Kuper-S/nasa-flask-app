# Base image: using debian-slim-bookworm for more security or consider distroless
FROM python:3.9-slim-bookworm

# Set labels and non-root user
LABEL maintainer="Super-Kuper" version="1.0.0"
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install essential tools and upgrade system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies with pinned versions
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Set ownership and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Run Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
