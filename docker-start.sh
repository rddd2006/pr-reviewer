#!/bin/bash
# Docker quick start

echo "🐳 Starting Diff Reviewer with Docker..."

# Check for .env
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys before starting"
fi

# Build and start services
docker-compose up -d --build

echo "✅ Services started!"
echo ""
echo "📍 API available at: http://localhost:8000"
echo "📊 API Docs at: http://localhost:8000/docs"
echo ""
echo "View logs:"
echo "  docker-compose logs -f"
echo ""
echo "Stop services:"
echo "  docker-compose down"
