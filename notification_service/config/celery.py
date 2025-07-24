import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("notification_service")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    "process-pending-notifications": {
        "task": "apps.api.tasks.process_pending_notifications",
        "schedule": 60.0,  # Run every 60 seconds
    },
    "check-overdue-tasks": {
        "task": "apps.api.tasks.check_overdue_tasks",
        "schedule": 300.0,  # Run every 5 minutes
    },
}

app.conf.update(timezone="UTC")


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
