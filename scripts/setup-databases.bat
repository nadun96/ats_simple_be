@echo off
REM setup-databases.bat - Comprehensive database setup and migration script for Windows

echo 🚀 Setting up ATS Backend with PostgreSQL databases...

REM Check if .env file exists
if not exist ".env" (
    echo ❌ .env file not found. Creating from .env.example...
    copy .env.example .env
    echo ✅ Created .env file. Please review and update the configuration.
)

echo.
echo 📋 Database configuration:
echo    - auth_db (Auth Service)
echo    - ats_db (Application Service)
echo    - email_db (Email Service)
echo.

echo 🐳 Starting Docker Compose services...
echo    This will:
echo    1. Start PostgreSQL with persistent volumes
echo    2. Initialize all required databases
echo    3. Run migrations for each service
echo    4. Start all microservices
echo.

REM Stop any existing containers
cd ..
docker-compose down

REM Start services
docker-compose up --build

echo.
echo ✅ All services should be running with proper database setup!
echo.
echo 🔗 Service URLs:
echo    - Auth Service: http://localhost:8000
echo    - Application Service: http://localhost:8001
echo    - Email Service: http://localhost:8002
echo    - PostgreSQL: localhost:5432
echo    - Redis: localhost:6379
echo    - RabbitMQ Management: http://localhost:15672
echo.
echo 📊 Database connections:
echo    - auth_db: psql -h localhost -p 5432 -U ats_user -d auth_db
echo    - ats_db: psql -h localhost -p 5432 -U ats_user -d ats_db
echo    - email_db: psql -h localhost -p 5432 -U ats_user -d email_db

pause
