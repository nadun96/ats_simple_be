# Database Setup Guide

This guide explains how to set up PostgreSQL databases for the ATS microservices with persistent data volumes.

## Quick Start

### Windows (PowerShell/Command Prompt)
```bash
setup-databases.bat
```

### Linux/Mac (Bash)
```bash
chmod +x setup-databases.sh
./setup-databases.sh
```

## Database Architecture

The system uses three separate PostgreSQL databases:

| Service | Database | Port | Purpose |
|---------|----------|------|---------|
| Auth Service | `auth_db` | 8000 | User authentication and authorization |
| Application Service | `ats_db` | 8001 | Main application data |
| Email Service | `email_db` | 8002 | Email templates and queue management |

## What Happens During Setup

1. **PostgreSQL Container**: Starts with persistent volume (`postgres_data`)
2. **Database Initialization**: Creates all three databases automatically
3. **Migration Execution**: Runs Django migrations for each service
4. **Service Startup**: Starts all microservices with proper database connections

## Manual Setup Steps

If you prefer to set up manually:

### 1. Start Infrastructure Services
```bash
docker-compose up postgres redis rabbitmq
```

### 2. Wait for PostgreSQL to be Ready
```bash
# Check PostgreSQL is accepting connections
docker exec ats_postgres pg_isready -U ats_user
```

### 3. Create Databases (if not auto-created)
```bash
docker exec -it ats_postgres psql -U ats_user -d postgres -c "
CREATE DATABASE auth_db;
CREATE DATABASE ats_db;
CREATE DATABASE email_db;
"
```

### 4. Start Application Services
```bash
docker-compose up auth_service application_service email_service
```

## Verification

### Check Database Status
```bash
# Linux/Mac
chmod +x check-databases.sh
./check-databases.sh

# Or manually check each database
PGPASSWORD=ats_password psql -h localhost -p 5432 -U ats_user -d auth_db
PGPASSWORD=ats_password psql -h localhost -p 5432 -U ats_user -d ats_db
PGPASSWORD=ats_password psql -h localhost -p 5432 -U ats_user -d email_db
```

### Check Running Services
```bash
docker-compose ps
```

Expected output should show all services as "Up":
- ats_postgres
- ats_redis  
- ats_rabbitmq
- auth_service
- application_service
- email_service
- email_worker
- email_beat
- email_queue_consumer

## Data Persistence

Data is stored in Docker volumes:

- `postgres_data`: PostgreSQL data files
- `redis_data`: Redis data files  
- `rabbitmq_data`: RabbitMQ data files

These volumes persist data between container restarts. To reset all data:

```bash
# Linux/Mac
chmod +x reset-databases.sh
./reset-databases.sh

# Or manually
docker-compose down
docker volume rm ats_simple_be_postgres_data ats_simple_be_redis_data ats_simple_be_rabbitmq_data
docker-compose up --build
```

## Environment Configuration

Database settings are configured in `.env`:

```env
# Database settings
DATABASE_USER=ats_user
DATABASE_PASSWORD=ats_password
DATABASE_HOST=postgres
DATABASE_PORT=5432

# Service-specific databases
DATABASE_NAME=ats_db
AUTH_DATABASE_NAME=auth_db
EMAIL_DATABASE_NAME=email_db
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   - PostgreSQL (5432), Redis (6379), RabbitMQ (5672, 15672)
   - Stop conflicting services or change ports in docker-compose.yml

2. **Permission Errors**
   - Make scripts executable: `chmod +x *.sh`
   - Check Docker daemon is running

3. **Database Connection Failed**
   - Verify PostgreSQL container is healthy: `docker-compose ps`
   - Check logs: `docker-compose logs postgres`

4. **Migration Errors**
   - Check service logs: `docker-compose logs auth_service`
   - Ensure databases exist before running migrations

### Health Checks

All services include health checks:

```bash
# Check PostgreSQL health
docker exec ats_postgres pg_isready -U ats_user

# Check Redis health  
docker exec ats_redis redis-cli ping

# Check RabbitMQ health
docker exec ats_rabbitmq rabbitmq-diagnostics ping
```

### Service URLs

- Auth Service: http://localhost:8000
- Application Service: http://localhost:8001  
- Email Service: http://localhost:8002
- RabbitMQ Management: http://localhost:15672 (guest/guest)

## Development Workflow

For development with live code changes:

1. **Start infrastructure only:**
   ```bash
   docker-compose up postgres redis rabbitmq
   ```

2. **Run services locally:**
   ```bash
   # Terminal 1
   cd auth_service
   python manage.py runserver 8000
   
   # Terminal 2  
   cd application_service
   python manage.py runserver 8001
   
   # Terminal 3
   cd email_service
   python manage.py runserver 8002
   ```

3. **Use local database connection:**
   Update `.env` to use `DATABASE_HOST=localhost` instead of `postgres`

## Backup and Restore

### Backup
```bash
# Backup all databases
docker exec ats_postgres pg_dumpall -U ats_user > backup.sql

# Backup specific database
docker exec ats_postgres pg_dump -U ats_user auth_db > auth_db_backup.sql
```

### Restore
```bash
# Restore all databases
docker exec -i ats_postgres psql -U ats_user < backup.sql

# Restore specific database
docker exec -i ats_postgres psql -U ats_user -d auth_db < auth_db_backup.sql
```
