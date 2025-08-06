from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("email_service")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery beat schedule for task scheduling
app.conf.beat_schedule = {
    "process-scheduled-emails": {
        "task": "apps.api.tasks.process_scheduled_emails",
        "schedule": 60.0,  # Run every minute
    },
}

app.conf.timezone = "UTC"
app.conf.enable_utc = True


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
