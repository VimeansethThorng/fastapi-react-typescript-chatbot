# Multi-stage Docker build for FastAPI-React TypeScript Chatbot

# Stage 1: Build the React frontend
FROM node:18-alpine as frontend-build

WORKDIR /frontend

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend source code
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Backend with Python
FROM python:3.11-slim as backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements_sqlite.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_sqlite.txt

# Copy backend source code
COPY backend/ ./

# Copy built frontend files - copy the entire build directory contents
COPY --from=frontend-build /frontend/build/ ./static/

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main_sqlite:app", "--host", "0.0.0.0", "--port", "8000"]