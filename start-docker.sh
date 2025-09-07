#!/bin/bash

# Start script untuk Stunting Checking App dengan Docker

echo "🐳 Starting Stunting Checking App with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install it first."
    exit 1
fi

# Build and start services
echo "🔨 Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Show logs
echo "📋 Service logs:"
docker-compose logs --tail=20

echo ""
echo "🎉 Services started successfully!"
echo "📊 MySQL is running on localhost:3306"
echo "🚀 API is running on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop services, run: docker-compose down"
echo "To view logs, run: docker-compose logs -f"
