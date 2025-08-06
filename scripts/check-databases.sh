#!/bin/bash
# check-databases.sh - Check database connectivity and status

set -e

echo "🔍 Checking Database Status..."

# Database connection parameters
HOST="localhost"
PORT="5432"
USER="ats_user"
PASSWORD="ats_password"

# Function to check database
check_database() {
    local db_name=$1
    echo -n "Checking $db_name... "
    
    if PGPASSWORD="$PASSWORD" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$db_name" -c '\q' 2>/dev/null; then
        echo "✅ Connected"
        
        # Check if there are any tables
        table_count=$(PGPASSWORD="$PASSWORD" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$db_name" -t -c "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public';")
        echo "   Tables: $table_count"
        
        # Check Django migrations table if it exists
        if PGPASSWORD="$PASSWORD" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$db_name" -c '\d django_migrations' 2>/dev/null | grep -q 'django_migrations'; then
            migration_count=$(PGPASSWORD="$PASSWORD" psql -h "$HOST" -p "$PORT" -U "$USER" -d "$db_name" -t -c "SELECT count(*) FROM django_migrations;")
            echo "   Migrations applied: $migration_count"
        else
            echo "   ⚠️  No migrations table found"
        fi
    else
        echo "❌ Failed to connect"
    fi
    echo ""
}

# Check if PostgreSQL container is running
if docker ps | grep -q "ats_postgres"; then
    echo "✅ PostgreSQL container is running"
else
    echo "❌ PostgreSQL container is not running"
    echo "Run 'docker-compose up postgres' to start it"
    exit 1
fi

echo ""

# Check each database
check_database "auth_db"
check_database "ats_db" 
check_database "email_db"

# Check service containers
echo "🐳 Service Container Status:"
services=("auth_service" "application_service" "email_service" "email_worker" "email_beat")

for service in "${services[@]}"; do
    if docker ps | grep -q "$service"; then
        echo "✅ $service is running"
    else
        echo "❌ $service is not running"
    fi
done

echo ""
echo "🔗 Quick database connection commands:"
echo "   auth_db:  PGPASSWORD=ats_password psql -h localhost -p 5432 -U ats_user -d auth_db"
echo "   ats_db:   PGPASSWORD=ats_password psql -h localhost -p 5432 -U ats_user -d ats_db" 
echo "   email_db: PGPASSWORD=ats_password psql -h localhost -p 5432 -U ats_user -d email_db"
