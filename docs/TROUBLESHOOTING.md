# ATS Microservices - Troubleshooting Guide

## 🔧 Common Issues and Solutions

### Service Connection Issues

#### Problem: "CONNECTION ERROR - Service may not be running"

**Solutions:**

1. **Start Services**
   ```bash
   # Start all services
   docker-compose up -d
   
   # Check service status
   docker-compose ps
   
   # View service logs
   docker-compose logs -f [service_name]
   ```

2. **Check Docker Status**
   ```bash
   # Verify Docker is running
   docker info
   
   # Check available containers
   docker ps -a
   ```

3. **Rebuild Services**
   ```bash
   # Rebuild and restart
   docker-compose down
   docker-compose up -d --build
   ```

### Database Issues

#### Problem: Database migration errors

**Solutions:**

1. **Run Migrations Manually**
   ```bash
   # Application service
   docker-compose exec application_service python manage.py migrate
   
   # Auth service
   docker-compose exec auth_service python manage.py migrate
   
   # Email service
   docker-compose exec email_service python manage.py migrate
   ```

2. **Reset Database (⚠️ Data Loss)**
   ```bash
   # Stop services
   docker-compose down
   
   # Remove database volume
   docker volume rm ats_simple_be_postgres_data
   
   # Restart services
   docker-compose up -d
   ```

### Port Conflicts

#### Problem: Port already in use

**Solutions:**

1. **Check Port Usage**
   ```bash
   # Windows
   netstat -ano | findstr :8000
   
   # Linux/Mac
   lsof -i :8000
   ```

2. **Change Ports in docker-compose.yml**
   ```yaml
   services:
     auth_service:
       ports:
         - "8010:8000"  # Change external port
   ```

3. **Kill Conflicting Processes**
   ```bash
   # Windows
   taskkill /PID [PID_NUMBER] /F
   
   # Linux/Mac
   kill -9 [PID_NUMBER]
   ```

### Environment Configuration

#### Problem: Environment variables not loaded

**Solutions:**

1. **Check .env File**
   ```bash
   # Verify .env file exists
   ls -la .env
   
   # Check content
   cat .env
   ```

2. **Copy from Template**
   ```bash
   cp .env.example .env
   ```

3. **Verify Variables in Container**
   ```bash
   docker-compose exec application_service env | grep DATABASE
   ```

### Email Service Issues

#### Problem: Email not sending

**Solutions:**

1. **Check Email Configuration**
   ```bash
   # Verify email settings in .env
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   ```

2. **Check Celery Workers**
   ```bash
   # View email worker logs
   docker-compose logs -f email_worker
   
   # Check queue status
   docker-compose exec email_service celery -A config inspect active
   ```

3. **Test Email Sending**
   ```python
   # Django shell
   docker-compose exec email_service python manage.py shell
   
   # Test email
   from django.core.mail import send_mail
   send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
   ```

### Queue Processing Issues

#### Problem: RabbitMQ not processing messages

**Solutions:**

1. **Check RabbitMQ Status**
   ```bash
   # View RabbitMQ logs
   docker-compose logs -f rabbitmq
   
   # Access management interface
   # http://localhost:15672 (guest/guest)
   ```

2. **Restart Queue Consumers**
   ```bash
   # Restart email queue consumer
   docker-compose restart email_queue_consumer
   
   # Check consumer logs
   docker-compose logs -f email_queue_consumer
   ```

### Application Service Issues

#### Problem: Model/Migration errors

**Solutions:**

1. **Check Model Definitions**
   ```bash
   # View Django models
   docker-compose exec application_service python manage.py showmigrations
   ```

2. **Create Missing Migrations**
   ```bash
   docker-compose exec application_service python manage.py makemigrations
   docker-compose exec application_service python manage.py migrate
   ```

3. **Reset Migrations (⚠️ Data Loss)**
   ```bash
   # Remove migration files
   docker-compose exec application_service find . -name "*.pyc" -delete
   docker-compose exec application_service find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
   
   # Recreate migrations
   docker-compose exec application_service python manage.py makemigrations
   docker-compose exec application_service python manage.py migrate
   ```

## 🔍 Debugging Commands

### Service Health Checks

```bash
# Check all container status
docker-compose ps

# View all service logs
docker-compose logs

# View specific service logs
docker-compose logs -f application_service

# Follow logs for all services
docker-compose logs -f

# Check resource usage
docker stats
```

### Database Debugging

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U ats_user -d ats_db

# List tables
\dt

# Check specific table
SELECT * FROM candidates LIMIT 5;

# Exit PostgreSQL
\q
```

### Redis Debugging

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Check keys
KEYS *

# Get value
GET some_key

# Check info
INFO

# Exit Redis
exit
```

### Application Debugging

```bash
# Django shell
docker-compose exec application_service python manage.py shell

# Check models
from apps.api.models import Job, Candidate, Application
print(Job.objects.count())
print(Candidate.objects.count())
print(Application.objects.count())

# Run Django tests
docker-compose exec application_service python manage.py test
```

## 📊 Performance Monitoring

### Resource Usage

```bash
# Monitor container resources
docker stats

# Check disk usage
docker system df

# View container processes
docker-compose exec application_service ps aux
```

### Database Performance

```bash
# Check database connections
docker-compose exec postgres psql -U ats_user -d ats_db -c "SELECT * FROM pg_stat_activity;"

# Check table sizes
docker-compose exec postgres psql -U ats_user -d ats_db -c "SELECT schemaname,tablename,attname,n_distinct,correlation FROM pg_stats;"
```

### API Performance

```bash
# Test API response times
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost:8001/api/v1/jobs/"

# Monitor with htop (if available)
docker-compose exec application_service htop
```

## 🔒 Security Troubleshooting

### Authentication Issues

```bash
# Check JWT token
docker-compose exec auth_service python manage.py shell

# Verify user creation
from django.contrib.auth.models import User
print(User.objects.all())

# Test token generation
from rest_framework_simplejwt.tokens import RefreshToken
user = User.objects.first()
token = RefreshToken.for_user(user)
print(f"Access: {token.access_token}")
```

### Permission Issues

```bash
# Check file permissions
docker-compose exec application_service ls -la

# Fix permission issues
docker-compose exec application_service chown -R app:app /app

# Check Django permissions
docker-compose exec application_service python manage.py shell
from django.contrib.auth.models import Permission
print(Permission.objects.all())
```

## 🚨 Emergency Procedures

### Complete Reset (⚠️ Data Loss)

```bash
# Stop all services
docker-compose down

# Remove all volumes (deletes all data)
docker-compose down -v

# Remove all containers and images
docker-compose down --rmi all

# Rebuild everything
docker-compose up -d --build
```

### Service Recovery

```bash
# Restart specific service
docker-compose restart application_service

# Recreate service
docker-compose up -d --force-recreate application_service

# Scale service (if needed)
docker-compose up -d --scale application_service=2
```

### Backup Procedures

```bash
# Backup database
docker-compose exec postgres pg_dump -U ats_user ats_db > backup.sql

# Backup volumes
docker run --rm -v ats_simple_be_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data

# Restore database
docker-compose exec -T postgres psql -U ats_user ats_db < backup.sql
```

## 📞 Getting Help

### Log Collection

```bash
# Collect all logs
docker-compose logs > ats_logs.txt

# Collect system info
docker version > system_info.txt
docker-compose version >> system_info.txt
docker system info >> system_info.txt
```

### Environment Info

```bash
# Check environment
env | grep -E "(DATABASE|REDIS|RABBITMQ|EMAIL)" > env_info.txt

# Check Docker setup
docker-compose config > docker_config.txt
```

### Service Status Report

```bash
# Generate status report
echo "=== Service Status ===" > status_report.txt
docker-compose ps >> status_report.txt
echo "" >> status_report.txt
echo "=== Container Info ===" >> status_report.txt
docker stats --no-stream >> status_report.txt
```

## 📋 Maintenance Tasks

### Regular Maintenance

```bash
# Clean up unused Docker resources
docker system prune -a

# Update images
docker-compose pull
docker-compose up -d

# Rotate logs
docker-compose logs --since 1h > recent_logs.txt
```

### Health Monitoring

```bash
# Create health check script
curl -f http://localhost:8000/health/ || echo "Auth service down"
curl -f http://localhost:8001/health/ || echo "Application service down"
curl -f http://localhost:8002/health/ || echo "Email service down"
curl -f http://localhost:8003/health/ || echo "Notification service down"
```

---

For additional help:
- Check service-specific README files
- Review Docker Compose logs
- Consult the main PROJECT_DOCUMENTATION.md
- Run the comprehensive test suite: `python test_all_services.py`
