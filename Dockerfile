# Stage 1: Builder
FROM python:3.9-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --user -r requirements.txt

# Stage 2: Production
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install runtime dependencies (if any)
# For most Flask apps, runtime dependencies are covered by the Python packages.
# If your application requires additional system packages, install them here.
# Example:
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends some-runtime-package && \
#     rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

# Update PATH to include the local bin
ENV PATH=/root/.local/bin:$PATH

# Copy project files
COPY . .

# Create directories for uploads and merged files
RUN mkdir -p uploads merged

# Expose the port Flask is running on
EXPOSE 5000

# Define the default command to run the app
CMD ["python", "app.py"]
