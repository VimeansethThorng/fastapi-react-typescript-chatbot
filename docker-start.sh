#!/bin/bash

# FastAPI React TypeScript Chatbot - Docker Startup Script

echo "🚀 Starting FastAPI React TypeScript Chatbot with Docker..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your OpenAI API key before running again."
    echo "   OPENAI_API_KEY=your_openai_api_key_here"
    exit 1
fi

# Check if OpenAI API key is set
if grep -q "your_openai_api_key_here" .env; then
    echo "⚠️  Please set your OpenAI API key in the .env file:"
    echo "   OPENAI_API_KEY=your_openai_api_key_here"
    exit 1
fi

# Create data directory if it doesn't exist
mkdir -p data

echo "🐳 Building and starting Docker containers..."

# Build and run the containers
docker-compose up --build

echo "✅ Application started!"
echo "🌐 Backend API: http://localhost:8000"
echo "🌐 Frontend (Production): http://localhost:8000"
echo "🌐 Frontend (Development): http://localhost:3000 (if running dev profile)"
echo ""
echo "To run with development frontend:"
echo "docker-compose --profile dev up --build"