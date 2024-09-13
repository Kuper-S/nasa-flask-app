# Base image
FROM python:3.9-slim

# Set labels and non-root user
LABEL maintainer="Super-Kuper" version="1.0.0"
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies (including gunicorn)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

# Copy application code
COPY . .

# Set permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser


# Command to run Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]

