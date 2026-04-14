#!/bin/bash

echo "📚 School Management System - Quick Setup"
echo "=========================================="
echo ""

# Check if docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker."
    exit 1
fi

echo "✅ Building Docker image..."
docker build -t school-management:latest .

echo "✅ Running container on port 8000..."
docker run -d -p 8000:8000 \
    -e SECRET_KEY="dev-secret-key-change-in-production" \
    -e DATABASE_URL="sqlite:///./school.db" \
    --name school-app \
    school-management:latest

sleep 2

echo ""
echo "✅ School Management System is running!"
echo ""
echo "📍 Access the app:"
echo "   Login: http://localhost:8000"
echo "   API:   http://localhost:8000/docs (Swagger UI)"
echo ""
echo "📝 Quick test:"
echo "   curl http://localhost:8000/health"
echo ""
echo "🛑 To stop:"
echo "   docker stop school-app"
echo "   docker rm school-app"
echo ""
