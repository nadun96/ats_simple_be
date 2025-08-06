#!/bin/bash

# Start Celery beat scheduler
exec celery -A config beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
