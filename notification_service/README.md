# ATS Notification Service

This service provides REST API endpoints for managing notifications and tasks within the ATS (Application Tracking System) workflow. It includes Redis-based Celery task queues for asynchronous processing.

## Features

- **Notification Management**: Create and manage notifications for workflow steps
- **Task Management**: Create and track tasks assigned to users
- **Celery Integration**: Asynchronous task processing with Redis
- **REST API**: Full CRUD operations with Swagger documentation
- **Email Notifications**: Send notifications via email
- **Filtering**: Advanced filtering for both notifications and tasks

## API Endpoints

### Notifications

#### List/Create Notifications
- **GET** `/api/notifications/` - List all notifications
  - Query parameters:
    - `channel`: Filter by channel (email, sms, push, in_app)
    - `step_id`: Filter by workflow step ID
    - `trigger_on_entry`: Filter by trigger setting (true/false)

- **POST** `/api/notifications/` - Create a new notification
  ```json
  {
    "step_id": 1,
    "channel": "email",
    "template_name": "welcome_notification",
    "trigger_on_entry": true
  }
  ```

#### Individual Notification Operations
- **GET** `/api/notifications/{notification_id}/` - Retrieve specific notification
- **PUT** `/api/notifications/{notification_id}/` - Update notification
- **PATCH** `/api/notifications/{notification_id}/` - Partial update notification
- **DELETE** `/api/notifications/{notification_id}/` - Delete notification

### Tasks

#### List/Create Tasks
- **GET** `/api/tasks/` - List all tasks
  - Query parameters:
    - `status`: Filter by status (pending, in_progress, completed, cancelled)
    - `assignee_id`: Filter by assignee user ID
    - `step_id`: Filter by workflow step ID

- **POST** `/api/tasks/` - Create a new task
  ```json
  {
    "step_id": 1,
    "assignee_id": 1,
    "description": "Review application documents",
    "due_date": "2025-07-30T10:00:00Z",
    "status": "pending"
  }
  ```

#### Individual Task Operations
- **GET** `/api/tasks/{task_id}/` - Retrieve specific task
- **PUT** `/api/tasks/{task_id}/` - Update task
- **PATCH** `/api/tasks/{task_id}/` - Partial update task
- **DELETE** `/api/tasks/{task_id}/` - Delete task

## Models

### Notification Model
- `notification_id`: Primary key (auto-generated)
- `step_id`: Foreign key reference to workflow step
- `channel`: Notification channel (email, sms, push, in_app)
- `template_name`: Name of the notification template
- `trigger_on_entry`: Whether to trigger when entering workflow step
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

### Task Model
- `task_id`: Primary key (auto-generated)
- `step_id`: Foreign key reference to workflow step
- `assignee_id`: Foreign key to User model
- `description`: Task description
- `due_date`: Due date for task completion (optional)
- `status`: Task status (pending, in_progress, completed, cancelled)
- `created_at`: Timestamp of creation
- `updated_at`: Timestamp of last update

## Celery Tasks

### Available Tasks

1. **send_notification_email**: Send email notifications
2. **send_sms_notification**: Send SMS notifications (placeholder)
3. **send_push_notification**: Send push notifications (placeholder)
4. **trigger_workflow_notifications**: Trigger all notifications for a workflow step
5. **create_task_for_step**: Create a task for a specific workflow step
6. **check_overdue_tasks**: Check for overdue tasks and send notifications
7. **complete_task**: Mark a task as completed

### Periodic Tasks

- **process-pending-notifications**: Runs every 60 seconds
- **check-overdue-tasks**: Runs every 5 minutes

## Setup Instructions

### Prerequisites
- Python 3.8+
- Redis server
- PostgreSQL database

### Environment Variables

Create a `.env` file in the notification_service directory:

```env
# Database
DATABASE_NAME=db_ats
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=noreply@ats-system.com
```

### Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Create superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

### Running the Services

1. **Start Redis server** (if not already running):
   ```bash
   redis-server
   ```

2. **Start Django development server**:
   ```bash
   python manage.py runserver
   ```

3. **Start Celery worker** (in another terminal):
   ```bash
   celery -A config worker --loglevel=info
   ```

4. **Start Celery Beat scheduler** (in another terminal):
   ```bash
   celery -A config beat --loglevel=info
   ```

### Demo Commands

Test the Celery integration with the demo command:

```bash
# Create a sample notification
python manage.py demo_celery --action=create_notification --step-id=1

# Create a sample task
python manage.py demo_celery --action=create_task --step-id=1

# Trigger notifications for a step
python manage.py demo_celery --action=trigger_notifications --step-id=1 --email=test@example.com

# Check for overdue tasks
python manage.py demo_celery --action=check_overdue
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **API Schema**: `http://localhost:8000/swagger.json`

## Example Usage

### Creating a Notification via API

```bash
curl -X POST http://localhost:8000/api/notifications/ \
  -H "Content-Type: application/json" \
  -d '{
    "step_id": 1,
    "channel": "email",
    "template_name": "application_received",
    "trigger_on_entry": true
  }'
```

### Creating a Task via API

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "step_id": 1,
    "assignee_id": 1,
    "description": "Review candidate application",
    "due_date": "2025-07-30T17:00:00Z",
    "status": "pending"
  }'
```

### Filtering Tasks

```bash
# Get all pending tasks
curl "http://localhost:8000/api/tasks/?status=pending"

# Get tasks for specific assignee
curl "http://localhost:8000/api/tasks/?assignee_id=1"

# Get tasks for specific workflow step
curl "http://localhost:8000/api/tasks/?step_id=1"
```

## Integration with Workflow System

The notification and task system is designed to integrate with a workflow management system where:

1. **step_id** represents different stages in the recruitment process
2. **Notifications** are triggered when a candidate moves to a new workflow step
3. **Tasks** are created for users to perform actions at specific workflow steps
4. **Email notifications** keep stakeholders informed of process updates

## Monitoring

- Monitor Celery tasks using Flower (install with `pip install flower`):
  ```bash
  celery -A config flower
  ```
  Access at `http://localhost:5555`

- Check task status in Django admin or through the API
- Monitor Redis queues and performance

## Error Handling

The system includes comprehensive error handling:
- Failed email notifications are logged
- Task creation failures are captured
- Periodic tasks include error recovery mechanisms
- API endpoints return appropriate HTTP status codes with error details
