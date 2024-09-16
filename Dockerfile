# Stage 1: Build dependencies
FROM python:3.9-slim-bullseye AS builder

# Set labels
LABEL maintainer="Super-Kuper" version="1.0.0"

# Create non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy only the requirements to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies without cache
RUN pip install --no-cache-dir -r requirements.txt && pip install gunicorn

# Stage 2: Final lightweight image
FROM python:3.9-alpine

# Install shadow package to enable useradd and groupadd
RUN apk add --no-cache shadow

# Create non-root user and group in the final image
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy necessary dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn

# Copy the application code from the host to the container
COPY . .

# Set the proper ownership of the files for the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the application port
EXPOSE 5000

# Command to run the app with Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
