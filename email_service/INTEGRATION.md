# Email Service Integration Guide

This document provides examples of how other microservices can integrate with the Email Service.

## Base URL
```
http://localhost:8002/api/
```

## Authentication
Currently, the service doesn't require authentication, but you can add JWT or token-based auth as needed.

## Integration Examples

### 1. Application Service Integration

When a new application is received:

```python
import requests
import json

def send_application_confirmation(applicant_email, applicant_name, position_title, application_id):
    """Send confirmation email when application is received"""
    
    url = "http://email_service:8002/api/emails/send_notification/"
    
    # Get template for application confirmation
    template_url = "http://email_service:8002/api/templates/?name=application_received"
    template_response = requests.get(template_url)
    
    if template_response.status_code == 200:
        templates = template_response.json()['results']
        if templates:
            template = templates[0]
            
            # Replace template variables
            subject = template['subject'].replace('{position_title}', position_title)
            message = template['body_text'].replace('{applicant_name}', applicant_name)
            message = message.replace('{position_title}', position_title)
            message = message.replace('{application_id}', application_id)
            
            data = {
                "recipient": applicant_email,
                "subject": subject,
                "message": message,
                "email_type": "confirmation",
                "notification_id": f"app_confirm_{application_id}"
            }
            
            response = requests.post(url, json=data)
            return response.status_code == 200
    
    return False
```

### 2. Task Management Integration

When a task is due or a meeting is scheduled:

```python
import requests
from datetime import datetime

def schedule_meeting_reminder(meeting_data):
    """Schedule email reminder for upcoming meeting"""
    
    url = "http://email_service:8002/api/scheduled-tasks/"
    
    # Schedule reminder 1 hour before meeting
    reminder_time = meeting_data['scheduled_time'] - timedelta(hours=1)
    
    data = {
        "task_id": f"meeting_{meeting_data['id']}",
        "task_type": "meeting_reminder",
        "scheduled_at": reminder_time.isoformat(),
        "recipient_email": meeting_data['attendee_email'],
        "email_data": {
            "applicant_name": meeting_data['applicant_name'],
            "interview_date": meeting_data['date'],
            "interview_time": meeting_data['time'],
            "interview_type": meeting_data['type'],
            "interview_location": meeting_data['location'],
            "interviewer_name": meeting_data['interviewer_name'],
            "position_title": meeting_data['position']
        }
    }
    
    response = requests.post(url, json=data)
    return response.status_code == 201

def send_task_reminder(task_data):
    """Send immediate task reminder"""
    
    url = "http://email_service:8002/api/emails/send_notification/"
    
    data = {
        "recipient": task_data['assignee_email'],
        "subject": f"Task Reminder: {task_data['name']}",
        "message": f"Reminder: {task_data['description']} is due on {task_data['due_date']}",
        "email_type": "task_reminder",
        "metadata": {
            "task_id": task_data['id'],
            "priority": task_data['priority']
        }
    }
    
    response = requests.post(url, json=data)
    return response.status_code == 200
```

### 3. Workflow Integration

When application status changes:

```python
import requests

def send_status_update(application_id, applicant_email, status, next_steps):
    """Send application status update to candidate"""
    
    url = "http://email_service:8002/api/emails/"
    
    # Create email with template
    data = {
        "recipient": applicant_email,
        "subject": f"Application Status Update - {status}",
        "body_html": f"""
        <div style="font-family: Arial, sans-serif;">
            <h2>Application Status Update</h2>
            <p>Your application status has been updated to: <strong>{status}</strong></p>
            <p>Next steps: {next_steps}</p>
        </div>
        """,
        "body_text": f"Your application status: {status}. Next steps: {next_steps}",
        "email_type": "application_status",
        "metadata": {
            "application_id": application_id,
            "status": status
        }
    }
    
    response = requests.post(url, json=data)
    return response.status_code == 201
```

### 4. Notification Service Integration

Replace existing notification with email service:

```python
import requests

class EmailNotificationService:
    def __init__(self, base_url="http://email_service:8002/api/"):
        self.base_url = base_url
    
    def send_notification(self, recipient, subject, message, notification_type="notification", **kwargs):
        """Send immediate notification email"""
        
        url = f"{self.base_url}emails/send_notification/"
        
        data = {
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "email_type": notification_type,
            **kwargs
        }
        
        response = requests.post(url, json=data)
        return response.status_code == 200
    
    def schedule_reminder(self, recipient, subject, message, scheduled_time, **kwargs):
        """Schedule a reminder email"""
        
        url = f"{self.base_url}emails/"
        
        data = {
            "recipient": recipient,
            "subject": subject,
            "body_text": message,
            "body_html": f"<p>{message}</p>",
            "email_type": "task_reminder",
            "scheduled_at": scheduled_time.isoformat(),
            **kwargs
        }
        
        response = requests.post(url, json=data)
        return response.status_code == 201

# Usage
email_service = EmailNotificationService()

# Send immediate notification
email_service.send_notification(
    recipient="user@example.com",
    subject="Application Received",
    message="Thank you for your application!",
    notification_type="confirmation"
)

# Schedule reminder
from datetime import datetime, timedelta
email_service.schedule_reminder(
    recipient="interviewer@company.com",
    subject="Interview Reminder",
    message="Interview with candidate scheduled for tomorrow",
    scheduled_time=datetime.now() + timedelta(hours=23)
)
```

## RabbitMQ Integration

For high-volume notifications, you can directly publish to RabbitMQ:

```python
import pika
import json

def publish_notification_to_queue(notification_data):
    """Publish notification directly to RabbitMQ for immediate processing"""
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='rabbitmq',
            credentials=pika.PlainCredentials('guest', 'guest')
        )
    )
    channel = connection.channel()
    
    # Ensure queue exists
    channel.queue_declare(queue='notification_queue', durable=True)
    
    message = {
        "recipient": notification_data['email'],
        "subject": notification_data['subject'],
        "message": notification_data['message'],
        "email_type": notification_data.get('type', 'notification'),
        "notification_id": notification_data.get('id')
    }
    
    channel.basic_publish(
        exchange='',
        routing_key='notification_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            priority=4,  # High priority
            delivery_mode=2  # Persistent
        )
    )
    
    connection.close()
```

## Error Handling

Always handle errors when integrating:

```python
import requests
import logging

logger = logging.getLogger(__name__)

def safe_send_email(recipient, subject, message, email_type="notification"):
    """Safely send email with error handling"""
    
    try:
        url = "http://email_service:8002/api/emails/send_notification/"
        data = {
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "email_type": email_type
        }
        
        response = requests.post(url, json=data, timeout=10)
        
        if response.status_code == 200:
            logger.info(f"Email sent successfully to {recipient}")
            return True
        else:
            logger.error(f"Failed to send email: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error("Email service timeout")
        return False
    except requests.exceptions.ConnectionError:
        logger.error("Email service connection error")
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending email: {str(e)}")
        return False
```

## Monitoring Integration

Check email service health:

```python
import requests

def check_email_service_health():
    """Check if email service is healthy"""
    
    try:
        response = requests.get("http://email_service:8002/health/detailed/", timeout=5)
        
        if response.status_code == 200:
            health_data = response.json()
            return health_data['status'] == 'healthy'
        
        return False
        
    except Exception:
        return False

# Usage in other services
if not check_email_service_health():
    logger.warning("Email service is not healthy, skipping email notification")
else:
    # Proceed with email sending
    send_email_notification(...)
```

## Bulk Operations

For bulk email operations:

```python
import requests
from concurrent.futures import ThreadPoolExecutor
import time

def send_bulk_notifications(notifications):
    """Send multiple notifications efficiently"""
    
    def send_single_notification(notification):
        return safe_send_email(
            recipient=notification['email'],
            subject=notification['subject'],
            message=notification['message'],
            email_type=notification.get('type', 'notification')
        )
    
    # Use thread pool for concurrent sending
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(send_single_notification, notifications))
    
    success_count = sum(results)
    logger.info(f"Sent {success_count}/{len(notifications)} notifications successfully")
    
    return success_count

# Usage
bulk_notifications = [
    {
        'email': 'user1@example.com',
        'subject': 'Status Update',
        'message': 'Your application is under review',
        'type': 'application_status'
    },
    {
        'email': 'user2@example.com',
        'subject': 'Interview Scheduled',
        'message': 'Your interview is scheduled for tomorrow',
        'type': 'meeting_reminder'
    }
]

send_bulk_notifications(bulk_notifications)
```

## Configuration

Add email service configuration to your service's settings:

```python
# settings.py
EMAIL_SERVICE_URL = os.environ.get('EMAIL_SERVICE_URL', 'http://email_service:8002/api/')
EMAIL_SERVICE_TIMEOUT = int(os.environ.get('EMAIL_SERVICE_TIMEOUT', '10'))
EMAIL_SERVICE_ENABLED = os.environ.get('EMAIL_SERVICE_ENABLED', 'true').lower() == 'true'
```

This integration guide provides a comprehensive overview of how to integrate with the Email Service from other microservices in your ATS system.
