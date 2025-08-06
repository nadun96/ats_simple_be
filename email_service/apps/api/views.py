from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import json
import logging

from .models import Email, EmailTemplate, ScheduledTask, EmailQueue
from .serializers import (
    EmailSerializer,
    EmailCreateSerializer,
    EmailTemplateSerializer,
    ScheduledTaskSerializer,
    ScheduledTaskCreateSerializer,
    NotificationEmailSerializer,
    EmailQueueSerializer,
)
from .tasks import queue_email, process_scheduled_task
from .rabbitmq_client import RabbitMQClient

logger = logging.getLogger(__name__)


class EmailTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet for managing email templates"""

    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        template_type = self.request.query_params.get("type", None)
        is_active = self.request.query_params.get("active", None)

        if template_type:
            queryset = queryset.filter(template_type=template_type)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        return queryset


class EmailViewSet(viewsets.ModelViewSet):
    """ViewSet for managing emails"""

    queryset = Email.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return EmailCreateSerializer
        return EmailSerializer

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-created_at")

        # Filter by status
        status_filter = self.request.query_params.get("status", None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by email type
        email_type = self.request.query_params.get("type", None)
        if email_type:
            queryset = queryset.filter(email_type=email_type)

        # Filter by recipient
        recipient = self.request.query_params.get("recipient", None)
        if recipient:
            queryset = queryset.filter(recipient__icontains=recipient)

        # Filter by task_id or notification_id
        task_id = self.request.query_params.get("task_id", None)
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        notification_id = self.request.query_params.get("notification_id", None)
        if notification_id:
            queryset = queryset.filter(notification_id=notification_id)

        return queryset

    def perform_create(self, serializer):
        """Create email and queue for sending"""
        email = serializer.save()

        # If scheduled for future, mark as scheduled
        if email.scheduled_at and email.scheduled_at > timezone.now():
            email.status = "scheduled"
            email.save()
        else:
            # Queue immediately
            queue_email.delay(email.id)

    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):
        """Retry sending a failed email"""
        try:
            email = self.get_object()

            if email.status != "failed":
                return Response(
                    {"error": "Only failed emails can be retried"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not email.can_retry():
                return Response(
                    {"error": "Email has exceeded maximum retry attempts"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Reset status and queue for retry
            email.status = "pending"
            email.save()
            queue_email.delay(email.id)

            return Response({"message": "Email queued for retry"})

        except Exception as exc:
            logger.error(f"Failed to retry email {pk}: {str(exc)}")
            return Response(
                {"error": "Failed to retry email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"])
    def send_notification(self, request):
        """Send immediate notification email"""
        serializer = NotificationEmailSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # Send notification via RabbitMQ for immediate processing
                rabbitmq_client = RabbitMQClient()
                message = serializer.validated_data

                rabbitmq_client.publish_message(
                    "notification_queue",
                    json.dumps(message),
                    priority=4,  # High priority for notifications
                )

                return Response(
                    {
                        "message": "Notification email queued successfully",
                        "recipient": message["recipient"],
                    }
                )

            except Exception as exc:
                logger.error(f"Failed to send notification: {str(exc)}")
                return Response(
                    {"error": "Failed to queue notification email"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def statistics(self, request):
        """Get email statistics"""
        try:
            stats = {
                "total_emails": Email.objects.count(),
                "sent_emails": Email.objects.filter(status="sent").count(),
                "pending_emails": Email.objects.filter(status="pending").count(),
                "failed_emails": Email.objects.filter(status="failed").count(),
                "scheduled_emails": Email.objects.filter(status="scheduled").count(),
            }

            # Add email type breakdown
            email_types = Email.objects.values("email_type").distinct()
            for email_type in email_types:
                type_name = email_type["email_type"]
                stats[f"{type_name}_count"] = Email.objects.filter(
                    email_type=type_name
                ).count()

            return Response(stats)

        except Exception as exc:
            logger.error(f"Failed to get statistics: {str(exc)}")
            return Response(
                {"error": "Failed to get statistics"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ScheduledTaskViewSet(viewsets.ModelViewSet):
    """ViewSet for managing scheduled tasks"""

    queryset = ScheduledTask.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return ScheduledTaskCreateSerializer
        return ScheduledTaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset().order_by("scheduled_at")

        # Filter by processed status
        is_processed = self.request.query_params.get("processed", None)
        if is_processed is not None:
            queryset = queryset.filter(is_processed=is_processed.lower() == "true")

        # Filter by task type
        task_type = self.request.query_params.get("type", None)
        if task_type:
            queryset = queryset.filter(task_type=task_type)

        # Filter by task_id
        task_id = self.request.query_params.get("task_id", None)
        if task_id:
            queryset = queryset.filter(task_id=task_id)

        return queryset

    @action(detail=True, methods=["post"])
    def process_now(self, request, pk=None):
        """Process a scheduled task immediately"""
        try:
            task = self.get_object()

            if task.is_processed:
                return Response(
                    {"error": "Task has already been processed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Process task immediately
            process_scheduled_task.delay(task.id)

            return Response({"message": "Task queued for immediate processing"})

        except Exception as exc:
            logger.error(f"Failed to process task {pk}: {str(exc)}")
            return Response(
                {"error": "Failed to process task"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"])
    def upcoming(self, request):
        """Get upcoming scheduled tasks"""
        try:
            now = timezone.now()
            hours = int(request.query_params.get("hours", 24))

            upcoming_tasks = ScheduledTask.objects.filter(
                is_processed=False,
                scheduled_at__gte=now,
                scheduled_at__lte=now + timezone.timedelta(hours=hours),
            ).order_by("scheduled_at")

            serializer = ScheduledTaskSerializer(upcoming_tasks, many=True)
            return Response(serializer.data)

        except Exception as exc:
            logger.error(f"Failed to get upcoming tasks: {str(exc)}")
            return Response(
                {"error": "Failed to get upcoming tasks"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class EmailQueueViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing email queue"""

    queryset = EmailQueue.objects.all()
    serializer_class = EmailQueueSerializer

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-created_at")

        # Filter by queue status
        is_queued = self.request.query_params.get("queued", None)
        if is_queued is not None:
            queryset = queryset.filter(is_queued=is_queued.lower() == "true")

        # Filter by priority
        priority = self.request.query_params.get("priority", None)
        if priority:
            queryset = queryset.filter(priority=int(priority))

        return queryset
