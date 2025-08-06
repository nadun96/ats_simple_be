from celery import shared_task
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import json
import logging
from .models import Email, ScheduledTask, EmailQueue
from .rabbitmq_client import RabbitMQClient

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_task(self, email_id):
    """
    Celery task to send an email
    """
    try:
        email = Email.objects.get(id=email_id)

        # Prepare email
        msg = EmailMultiAlternatives(
            subject=email.subject,
            body=email.body_text,
            from_email=email.sender or settings.DEFAULT_FROM_EMAIL,
            to=[email.recipient],
        )

        # Add HTML content if available
        if email.body_html:
            msg.attach_alternative(email.body_html, "text/html")

        # Add CC and BCC if available
        if email.cc:
            try:
                cc_list = (
                    json.loads(email.cc) if isinstance(email.cc, str) else email.cc
                )
                msg.cc = cc_list
            except (json.JSONDecodeError, TypeError):
                pass

        if email.bcc:
            try:
                bcc_list = (
                    json.loads(email.bcc) if isinstance(email.bcc, str) else email.bcc
                )
                msg.bcc = bcc_list
            except (json.JSONDecodeError, TypeError):
                pass

        # Send email
        msg.send()

        # Mark as sent
        email.mark_as_sent()

        logger.info(f"Email sent successfully to {email.recipient}")
        return f"Email sent to {email.recipient}"

    except Email.DoesNotExist:
        logger.error(f"Email with ID {email_id} not found")
        return f"Email with ID {email_id} not found"

    except Exception as exc:
        logger.error(f"Failed to send email {email_id}: {str(exc)}")

        try:
            email = Email.objects.get(id=email_id)
            email.mark_as_failed(str(exc))

            # Retry if possible
            if email.can_retry():
                logger.info(f"Retrying email {email_id} (attempt {email.retry_count})")
                raise self.retry(
                    countdown=60 * email.retry_count
                )  # Exponential backoff

        except Email.DoesNotExist:
            pass

        raise exc


@shared_task
def send_notification_email(
    recipient,
    subject,
    message,
    email_type,
    sender=None,
    cc=None,
    bcc=None,
    notification_id=None,
    metadata=None,
):
    """
    Task to send immediate notification emails
    """
    try:
        # Create email record
        email = Email.objects.create(
            sender=sender or settings.DEFAULT_FROM_EMAIL,
            recipient=recipient,
            cc=json.dumps(cc) if cc else None,
            bcc=json.dumps(bcc) if bcc else None,
            subject=subject,
            body_html=f"<p>{message}</p>",
            body_text=message,
            email_type=email_type,
            notification_id=notification_id,
            metadata=metadata,
            status="pending",
        )

        # Queue for sending
        queue_email.delay(email.id)

        logger.info(f"Notification email queued for {recipient}")
        return f"Notification email queued for {recipient}"

    except Exception as exc:
        logger.error(f"Failed to create notification email: {str(exc)}")
        raise exc


@shared_task
def queue_email(email_id, priority=2):
    """
    Task to queue email for sending via RabbitMQ
    """
    try:
        email = Email.objects.get(id=email_id)

        # Create queue entry
        queue_entry, created = EmailQueue.objects.get_or_create(
            email=email, defaults={"priority": priority}
        )

        # Send to RabbitMQ
        rabbitmq_client = RabbitMQClient()
        message = {
            "email_id": email_id,
            "priority": priority,
            "recipient": email.recipient,
            "subject": email.subject,
        }

        rabbitmq_client.publish_message("email_queue", json.dumps(message), priority)

        # Mark as queued
        queue_entry.is_queued = True
        queue_entry.queued_at = timezone.now()
        queue_entry.save()

        logger.info(f"Email {email_id} queued in RabbitMQ")
        return f"Email {email_id} queued successfully"

    except Email.DoesNotExist:
        logger.error(f"Email with ID {email_id} not found")
        return f"Email with ID {email_id} not found"

    except Exception as exc:
        logger.error(f"Failed to queue email {email_id}: {str(exc)}")
        raise exc


@shared_task
def process_scheduled_emails():
    """
    Task to process scheduled emails and tasks
    """
    try:
        now = timezone.now()

        # Process scheduled emails
        scheduled_emails = Email.objects.filter(
            status="scheduled", scheduled_at__lte=now
        )

        for email in scheduled_emails:
            email.status = "pending"
            email.save()
            queue_email.delay(email.id)

        logger.info(f"Processed {scheduled_emails.count()} scheduled emails")

        # Process scheduled tasks
        scheduled_tasks = ScheduledTask.objects.filter(
            is_processed=False, scheduled_at__lte=now
        )

        for task in scheduled_tasks:
            process_scheduled_task.delay(task.id)

        logger.info(f"Processed {scheduled_tasks.count()} scheduled tasks")

        return f"Processed {scheduled_emails.count()} emails and {scheduled_tasks.count()} tasks"

    except Exception as exc:
        logger.error(f"Failed to process scheduled emails: {str(exc)}")
        raise exc


@shared_task
def process_scheduled_task(task_id):
    """
    Task to process a scheduled task and send corresponding email
    """
    try:
        task = ScheduledTask.objects.get(id=task_id)

        if task.is_processed:
            return f"Task {task_id} already processed"

        # Get email template if specified
        if task.email_template:
            template = task.email_template
            subject = template.subject
            body_html = template.body_html
            body_text = template.body_text

            # Replace placeholders with data if available
            if task.email_data:
                for key, value in task.email_data.items():
                    placeholder = f"{{{key}}}"
                    subject = subject.replace(placeholder, str(value))
                    body_html = body_html.replace(placeholder, str(value))
                    body_text = body_text.replace(placeholder, str(value))
        else:
            # Default content based on task type
            subject = f"Task Reminder: {task.task_type}"
            body_text = f"This is a reminder for your {task.task_type} task."
            body_html = f"<p>This is a reminder for your <strong>{task.task_type}</strong> task.</p>"

        # Create email
        email = Email.objects.create(
            sender=settings.DEFAULT_FROM_EMAIL,
            recipient=task.recipient_email,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
            email_type="task_reminder",
            task_id=task.task_id,
            metadata=task.email_data,
        )

        # Queue email for sending
        queue_email.delay(email.id, priority=3)  # High priority for task reminders

        # Mark task as processed
        task.mark_as_processed()

        logger.info(f"Processed scheduled task {task_id}")
        return f"Processed task {task_id} and queued email"

    except ScheduledTask.DoesNotExist:
        logger.error(f"Scheduled task {task_id} not found")
        return f"Task {task_id} not found"

    except Exception as exc:
        logger.error(f"Failed to process scheduled task {task_id}: {str(exc)}")
        raise exc


@shared_task
def cleanup_old_emails(days=30):
    """
    Task to cleanup old email records
    """
    try:
        from datetime import timedelta

        cutoff_date = timezone.now() - timedelta(days=days)

        # Delete old sent emails
        deleted_count = Email.objects.filter(
            status="sent", sent_at__lt=cutoff_date
        ).delete()[0]

        logger.info(f"Cleaned up {deleted_count} old email records")
        return f"Cleaned up {deleted_count} old emails"

    except Exception as exc:
        logger.error(f"Failed to cleanup old emails: {str(exc)}")
        raise exc


@shared_task
def retry_failed_emails():
    """
    Task to retry failed emails that can be retried
    """
    try:
        failed_emails = Email.objects.filter(status="failed")
        retried_count = 0

        for email in failed_emails:
            if email.can_retry():
                email.status = "pending"
                email.save()
                queue_email.delay(email.id)
                retried_count += 1

        logger.info(f"Retried {retried_count} failed emails")
        return f"Retried {retried_count} failed emails"

    except Exception as exc:
        logger.error(f"Failed to retry emails: {str(exc)}")
        raise exc
