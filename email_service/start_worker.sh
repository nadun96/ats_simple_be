#!/bin/bash

# Start Celery worker
exec celery -A config worker --loglevel=info --concurrency=4
