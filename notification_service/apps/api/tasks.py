from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
import logging

from .models.notification import Notification
from .models.task import Task
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


@shared_task
def send_notification_email(notification_id, recipient_email, context=None):
    """
    Send notification email using the specified template
    """
    try:
        notification = Notification.objects.get(notification_id=notification_id)

        if context is None:
            context = {}

        # Basic email template (you can customize this)
        subject = f"Notification: {notification.template_name}"
        message = f"""
        Hello,
        
        This is a notification from the ATS system.
        Template: {notification.template_name}
        Channel: {notification.channel}
        
        Context: {context}
        
        Best regards,
        ATS System
        """

        send_mail(
            subject=subject,
            message=message,
            from_email="noreply@ats-system.com",
            recipient_list=[recipient_email],
            fail_silently=False,
        )

        logger.info(f"Email notification sent successfully to {recipient_email}")
        return True

    except Notification.DoesNotExist:
        logger.error(f"Notification with ID {notification_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to send email notification: {str(e)}")
        return False


@shared_task
def send_sms_notification(notification_id, phone_number, context=None):
    """
    Send SMS notification (placeholder implementation)
    """
    try:
        notification = Notification.objects.get(notification_id=notification_id)

        # SMS implementation would go here
        # For now, just log the attempt
        logger.info(
            f"SMS notification would be sent to {phone_number} for template {notification.template_name}"
        )

        return True

    except Notification.DoesNotExist:
        logger.error(f"Notification with ID {notification_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to send SMS notification: {str(e)}")
        return False


@shared_task
def send_push_notification(notification_id, user_id, context=None):
    """
    Send push notification (placeholder implementation)
    """
    try:
        notification = Notification.objects.get(notification_id=notification_id)
        user = User.objects.get(id=user_id)

        # Push notification implementation would go here
        # For now, just log the attempt
        logger.info(
            f"Push notification would be sent to user {user.username} for template {notification.template_name}"
        )

        return True

    except (Notification.DoesNotExist, User.DoesNotExist) as e:
        logger.error(f"Notification or User not found: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Failed to send push notification: {str(e)}")
        return False


@shared_task
def trigger_workflow_notifications(step_id, context=None):
    """
    Trigger all notifications for a specific workflow step
    """
    try:
        notifications = Notification.objects.filter(
            step_id=step_id, trigger_on_entry=True
        )

        results = []
        for notification in notifications:
            if notification.channel == "email":
                # You would need to determine the recipient email from context
                recipient_email = context.get("recipient_email") if context else None
                if recipient_email:
                    result = send_notification_email.delay(
                        notification.notification_id, recipient_email, context
                    )
                    results.append(result)

            elif notification.channel == "sms":
                phone_number = context.get("phone_number") if context else None
                if phone_number:
                    result = send_sms_notification.delay(
                        notification.notification_id, phone_number, context
                    )
                    results.append(result)

            elif notification.channel == "push":
                user_id = context.get("user_id") if context else None
                if user_id:
                    result = send_push_notification.delay(
                        notification.notification_id, user_id, context
                    )
                    results.append(result)

        logger.info(f"Triggered {len(results)} notifications for step {step_id}")
        return len(results)

    except Exception as e:
        logger.error(
            f"Failed to trigger workflow notifications for step {step_id}: {str(e)}"
        )
        return 0


@shared_task
def process_pending_notifications():
    """
    Periodic task to process any pending notifications
    """
    try:
        # This could process notifications that failed to send initially
        logger.info("Processing pending notifications...")

        # Add your logic here to retry failed notifications
        # For example, you could have a NotificationLog model to track attempts

        return "Pending notifications processed"

    except Exception as e:
        logger.error(f"Failed to process pending notifications: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def create_task_for_step(
    step_id, assignee_id, description, due_date=None, context=None
):
    """
    Create a new task for a workflow step
    """
    try:
        assignee = User.objects.get(id=assignee_id)

        task = Task.objects.create(
            step_id=step_id,
            assignee_id=assignee,
            description=description,
            due_date=due_date,
            status="pending",
        )

        logger.info(
            f"Task {task.task_id} created for step {step_id} and assigned to {assignee.username}"
        )

        # Optionally send notification about task creation
        if context and context.get("notify_assignee"):
            send_notification_email.delay(
                notification_id=context.get("notification_id"),
                recipient_email=assignee.email,
                context={
                    "task_id": task.task_id,
                    "description": description,
                    "due_date": due_date,
                },
            )

        return task.task_id

    except User.DoesNotExist:
        logger.error(f"User with ID {assignee_id} not found")
        return None
    except Exception as e:
        logger.error(f"Failed to create task for step {step_id}: {str(e)}")
        return None


@shared_task
def check_overdue_tasks():
    """
    Periodic task to check for overdue tasks and send notifications
    """
    try:
        now = timezone.now()
        overdue_tasks = Task.objects.filter(
            due_date__lt=now, status__in=["pending", "in_progress"]
        )

        notification_count = 0
        for task in overdue_tasks:
            if task.due_date:  # Check if due_date is not None
                # Send overdue notification to assignee
                send_notification_email.delay(
                    notification_id=1,  # You might want to create a specific overdue notification
                    recipient_email=task.assignee_id.email,
                    context={
                        "task_id": task.task_id,
                        "description": task.description,
                        "due_date": task.due_date,
                        "days_overdue": (now - task.due_date).days,
                    },
                )
                notification_count += 1

        logger.info(f"Sent {notification_count} overdue task notifications")
        return f"Processed {len(overdue_tasks)} overdue tasks"

    except Exception as e:
        logger.error(f"Failed to check overdue tasks: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def complete_task(task_id, completed_by_user_id=None):
    """
    Mark a task as completed and trigger any follow-up notifications
    """
    try:
        task = Task.objects.get(task_id=task_id)
        task.status = "completed"
        task.save()

        logger.info(f"Task {task_id} marked as completed")

        # Optionally send completion notification
        if completed_by_user_id:
            # You could send notification to supervisors, etc.
            logger.info(f"Task {task_id} completed by user {completed_by_user_id}")

        return True

    except Task.DoesNotExist:
        logger.error(f"Task with ID {task_id} not found")
        return False
    except Exception as e:
        logger.error(f"Failed to complete task {task_id}: {str(e)}")
        return False
