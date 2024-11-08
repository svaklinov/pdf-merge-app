# Stage 1: Builder
FROM python:3.9-alpine AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apk update && \
    apk add --no-cache gcc musl-dev postgresql-dev && \
    rm -rf /var/cache/apk/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --user -r requirements.txt

# Stage 2: Production
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

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
