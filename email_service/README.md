# Email Service

A microservice for handling scheduled emails and notifications in the ATS system. This service manages email templates, schedules email sending based on tasks, and sends immediate notifications.

## Features

- **Email Templates**: Manage reusable email templates with variables
- **Scheduled Emails**: Schedule emails based on task due dates and meeting reminders
- **Immediate Notifications**: Send instant notification emails triggered by frontend requests
- **Queue Management**: RabbitMQ-based email queue with priority support
- **Retry Logic**: Automatic retry for failed emails with exponential backoff
- **Health Monitoring**: Health check endpoints for service monitoring

## Architecture

- **Django REST API**: Main service interface
- **PostgreSQL**: Database for email records and templates
- **RabbitMQ**: Message queue for email processing
- **Redis**: Celery result backend
- **Celery**: Distributed task queue for email processing
- **Celery Beat**: Scheduler for periodic tasks

## API Endpoints

### Email Templates
- `GET /api/templates/` - List email templates
- `POST /api/templates/` - Create email template
- `GET /api/templates/{id}/` - Get template details
- `PUT /api/templates/{id}/` - Update template
- `DELETE /api/templates/{id}/` - Delete template

### Emails
- `GET /api/emails/` - List emails with filtering
- `POST /api/emails/` - Create and queue email
- `GET /api/emails/{id}/` - Get email details
- `POST /api/emails/{id}/retry/` - Retry failed email
- `POST /api/emails/send_notification/` - Send immediate notification
- `GET /api/emails/statistics/` - Get email statistics

### Scheduled Tasks
- `GET /api/scheduled-tasks/` - List scheduled tasks
- `POST /api/scheduled-tasks/` - Create scheduled task
- `GET /api/scheduled-tasks/{id}/` - Get task details
- `POST /api/scheduled-tasks/{id}/process_now/` - Process task immediately
- `GET /api/scheduled-tasks/upcoming/` - Get upcoming tasks

### Email Queue
- `GET /api/queue/` - View email queue status

### Health
- `GET /health/` - Basic health check
- `GET /health/detailed/` - Detailed health check with dependencies

## Email Types

1. **notification** - General notifications
2. **task_reminder** - Task due reminders
3. **application_status** - Application status updates
4. **meeting_reminder** - Meeting/interview reminders
5. **confirmation** - Confirmation emails

## Template Variables

Templates support variable substitution using `{variable_name}` syntax:

### Application Templates
- `{applicant_name}` - Applicant's name
- `{position_title}` - Job position title
- `{company_name}` - Company name
- `{application_id}` - Unique application ID
- `{submission_date}` - Application submission date
- `{review_timeframe}` - Expected review time

### Interview Templates
- `{interview_date}` - Interview date
- `{interview_time}` - Interview time
- `{interview_duration}` - Interview duration
- `{interview_type}` - Interview type (video, phone, in-person)
- `{interview_location}` - Interview location or link
- `{interviewer_name}` - Interviewer's name

### Task Templates
- `{task_name}` - Task name
- `{task_description}` - Task description
- `{assignee_name}` - Task assignee name
- `{due_date}` - Task due date
- `{priority}` - Task priority

## Usage Examples

### Send Immediate Notification

```python
import requests

data = {
    "recipient": "user@example.com",
    "subject": "Application Status Update",
    "message": "Your application has been reviewed.",
    "email_type": "notification",
    "notification_id": "notif_123"
}

response = requests.post(
    "http://localhost:8002/api/emails/send_notification/",
    json=data
)
```

### Schedule a Task Reminder

```python
import requests
from datetime import datetime, timedelta

data = {
    "task_id": "task_123",
    "task_type": "meeting_reminder",
    "scheduled_at": (datetime.now() + timedelta(hours=1)).isoformat(),
    "recipient_email": "interviewer@company.com",
    "email_data": {
        "task_name": "Interview with John Doe",
        "assignee_name": "Jane Smith",
        "due_date": "2024-01-15 10:00:00",
        "priority": "High"
    }
}

response = requests.post(
    "http://localhost:8002/api/scheduled-tasks/",
    json=data
)
```

### Create Custom Email

```python
import requests

data = {
    "recipient": "candidate@example.com",
    "subject": "Interview Scheduled",
    "body_html": "<p>Your interview is scheduled for tomorrow.</p>",
    "body_text": "Your interview is scheduled for tomorrow.",
    "email_type": "meeting_reminder",
    "scheduled_at": "2024-01-15T09:00:00Z"
}

response = requests.post(
    "http://localhost:8002/api/emails/",
    json=data
)
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

- `EMAIL_HOST` - SMTP server hostname
- `EMAIL_PORT` - SMTP server port
- `EMAIL_HOST_USER` - SMTP username
- `EMAIL_HOST_PASSWORD` - SMTP password
- `RABBITMQ_HOST` - RabbitMQ hostname
- `DATABASE_HOST` - PostgreSQL hostname

## Development Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Load Default Templates**:
   ```bash
   python manage.py load_email_templates
   ```

4. **Start Services**:
   ```bash
   # Main Django service
   python manage.py runserver 0.0.0.0:8002
   
   # Celery worker
   celery -A config worker --loglevel=info
   
   # Celery beat scheduler
   celery -A config beat --loglevel=info
   
   # RabbitMQ consumer
   python manage.py consume_email_queue --queue=email_queue
   ```

## Docker Setup

1. **Build and Start**:
   ```bash
   docker-compose up -d
   ```

2. **View Logs**:
   ```bash
   docker-compose logs email_service
   docker-compose logs email_worker
   ```

## Monitoring

- **RabbitMQ Management**: http://localhost:15672 (guest/guest)
- **Email Service Health**: http://localhost:8002/health/detailed/
- **Service Logs**: Check Docker logs for each service

## Task Scheduling

The service automatically processes:
- **Scheduled emails** every minute
- **Task reminders** based on due dates
- **Failed email retries** with exponential backoff
- **Old email cleanup** (configurable retention period)

## Integration with Other Services

### Frontend Notifications
Send immediate notifications via POST to `/api/emails/send_notification/`

### Task Management
Create scheduled tasks via POST to `/api/scheduled-tasks/` when:
- Meetings are scheduled
- Deadlines are set
- Interviews are planned

### Application Workflow
Trigger emails during application state changes:
- Application received
- Status updates
- Interview invitations
- Final decisions

## Error Handling

- Failed emails are automatically retried up to 3 times
- Dead letter queues handle permanently failed messages
- Comprehensive logging for debugging
- Health checks monitor service dependencies

## Security Considerations

- Use app passwords for Gmail SMTP
- Secure RabbitMQ with proper credentials
- Validate email addresses before sending
- Rate limiting for API endpoints (implement as needed)
- Sanitize template variables to prevent injection

## Performance

- Queue-based processing prevents blocking
- Priority queues for urgent emails
- Batch processing for bulk operations
- Database indexing for efficient queries
- Configurable worker concurrency
