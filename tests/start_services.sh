#!/bin/bash

# ATS Microservices Quick Start Script
echo "🚀 Starting ATS Microservices..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

echo "✅ docker-compose is available"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration if needed."
fi

# Build and start all services
echo "🏗️ Building and starting all services..."
docker-compose up -d --build

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🏥 Checking service health..."

services=("postgres:5432" "redis:6379" "rabbitmq:5672")
for service in "${services[@]}"; do
    IFS=':' read -r host port <<< "$service"
    if nc -z localhost $port; then
        echo "✅ $host is running on port $port"
    else
        echo "❌ $host is not responding on port $port"
    fi
done

# Check HTTP services
http_services=("8000:Auth" "8001:Application" "8002:Email" "8003:Notification")
for service in "${http_services[@]}"; do
    IFS=':' read -r port name <<< "$service"
    if curl -f -s "http://localhost:$port" > /dev/null; then
        echo "✅ $name service is running on port $port"
    else
        echo "❌ $name service is not responding on port $port"
    fi
done

echo "📊 Service Status:"
docker-compose ps

echo ""
echo "🎉 ATS Services are starting up!"
echo ""
echo "📝 Service URLs:"
echo "   • Auth Service:        http://localhost:8000"
echo "   • Application Service: http://localhost:8001"
echo "   • Email Service:       http://localhost:8002"
echo "   • Notification Service: http://localhost:8003"
echo "   • RabbitMQ Management: http://localhost:15672 (guest/guest)"
echo ""
echo "🧪 Run tests:"
echo "   python test_all_services.py"
echo ""
echo "📚 View logs:"
echo "   docker-compose logs -f [service_name]"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
