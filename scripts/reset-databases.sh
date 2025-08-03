#!/bin/bash
# reset-databases.sh - Reset all databases and volumes

set -e

echo "⚠️  This will DESTROY all database data and volumes!"
echo "Are you sure you want to continue? (y/N)"
read -r response

if [[ ! "$response" =~ ^[Yy]$ ]]; then
    echo "Operation cancelled."
    exit 0
fi

echo "🛑 Stopping all services..."
docker-compose down

echo "🗑️  Removing volumes..."
docker volume rm ats_simple_be_postgres_data 2>/dev/null || echo "Postgres volume not found"
docker volume rm ats_simple_be_redis_data 2>/dev/null || echo "Redis volume not found" 
docker volume rm ats_simple_be_rabbitmq_data 2>/dev/null || echo "RabbitMQ volume not found"

echo "🧹 Pruning unused volumes..."
docker volume prune -f

echo "🏗️  Rebuilding and starting services..."
cd ..
docker-compose up --build

echo "✅ Databases have been reset and reinitialized!"
