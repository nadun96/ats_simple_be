@echo off
REM ATS Microservices Quick Start Script for Windows

echo 🚀 Starting ATS Microservices...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Check if docker-compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ docker-compose is not installed. Please install docker-compose and try again.
    pause
    exit /b 1
)

echo ✅ docker-compose is available

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ✅ .env file created. Please edit it with your configuration if needed.
)

REM Build and start all services
echo 🏗️ Building and starting all services...
docker-compose up -d --build

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

REM Check service health
echo 🏥 Checking service health...

echo 📊 Service Status:
docker-compose ps

echo.
echo 🎉 ATS Services are starting up!
echo.
echo 📝 Service URLs:
echo    • Auth Service:        http://localhost:8000
echo    • Application Service: http://localhost:8001
echo    • Email Service:       http://localhost:8002
echo    • Notification Service: http://localhost:8003
echo    • RabbitMQ Management: http://localhost:15672 (guest/guest)
echo.
echo 🧪 Run tests:
echo    python test_all_services.py
echo.
echo 📚 View logs:
echo    docker-compose logs -f [service_name]
echo.
echo 🛑 Stop services:
echo    docker-compose down

pause
