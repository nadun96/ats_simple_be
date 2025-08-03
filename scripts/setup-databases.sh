#!/bin/bash
# setup-databases.sh - Comprehensive database setup and migration script

set -e

echo "🚀 Setting up ATS Backend with PostgreSQL databases..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file. Please review and update the configuration."
fi

# Make scripts executable
chmod +x scripts/init-db.sh
chmod +x scripts/wait-for-db.sh

echo "📋 Database configuration:"
echo "   - auth_db (Auth Service)"
echo "   - ats_db (Application Service)" 
echo "   - email_db (Email Service)"
echo ""

echo "🐳 Starting Docker Compose services..."
echo "   This will:"
echo "   1. Start PostgreSQL with persistent volumes"
echo "   2. Initialize all required databases"
echo "   3. Run migrations for each service"
echo "   4. Start all microservices"
echo ""

# Stop any existing containers
cd ..
docker-compose down

# Start services
docker-compose up --build

echo ""
echo "✅ All services should be running with proper database setup!"
echo ""
echo "🔗 Service URLs:"
echo "   - Auth Service: http://localhost:8000"
echo "   - Application Service: http://localhost:8001"
echo "   - Email Service: http://localhost:8002"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo "   - RabbitMQ Management: http://localhost:15672"
echo ""
echo "📊 Database connections:"
echo "   - auth_db: psql -h localhost -p 5432 -U ats_user -d auth_db"
echo "   - ats_db: psql -h localhost -p 5432 -U ats_user -d ats_db"
echo "   - email_db: psql -h localhost -p 5432 -U ats_user -d email_db"
