from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import connection
from django.utils import timezone
import redis
import pika
from django.conf import settings


@api_view(["GET"])
def health_check(request):
    """Basic health check endpoint"""
    return Response(
        {"status": "healthy", "timestamp": timezone.now(), "service": "email_service"}
    )


@api_view(["GET"])
def health_detailed(request):
    """Detailed health check with dependencies"""
    health_status = {
        "status": "healthy",
        "timestamp": timezone.now(),
        "service": "email_service",
        "checks": {},
    }

    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Redis
    try:
        r = redis.Redis(host="redis", port=6379, db=0)
        r.ping()
        health_status["checks"]["redis"] = "healthy"
    except Exception as e:
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check RabbitMQ
    try:
        credentials = pika.PlainCredentials(
            settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD
        )
        parameters = pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            virtual_host=settings.RABBITMQ_VHOST,
            credentials=credentials,
        )
        rabbit_connection = pika.BlockingConnection(parameters)
        rabbit_connection.close()
        health_status["checks"]["rabbitmq"] = "healthy"
    except Exception as e:
        health_status["checks"]["rabbitmq"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"

    return Response(health_status)
