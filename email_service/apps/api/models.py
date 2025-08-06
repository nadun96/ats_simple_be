from django.db import models
from django.utils import timezone


class EmailTemplate(models.Model):
    """Email template model for storing reusable email templates"""

    TEMPLATE_TYPES = [
        ("notification", "Notification"),
        ("task_reminder", "Task Reminder"),
        ("application_status", "Application Status"),
        ("meeting_reminder", "Meeting Reminder"),
        ("confirmation", "Confirmation"),
    ]

    name = models.CharField(max_length=255, unique=True)
    template_type = models.CharField(max_length=50, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=255)
    body_html = models.TextField()
    body_text = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "email_templates"

    def __str__(self):
        return f"{self.name} ({self.template_type})"


class Email(models.Model):
    """Email model for storing email records"""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
        ("scheduled", "Scheduled"),
    ]

    EMAIL_TYPES = [
        ("notification", "Notification"),
        ("task_reminder", "Task Reminder"),
        ("application_status", "Application Status"),
        ("meeting_reminder", "Meeting Reminder"),
        ("confirmation", "Confirmation"),
    ]

    sender = models.EmailField()
    recipient = models.EmailField()
    cc = models.TextField(blank=True, null=True)  # JSON array of CC emails
    bcc = models.TextField(blank=True, null=True)  # JSON array of BCC emails
    subject = models.CharField(max_length=255)
    body_html = models.TextField()
    body_text = models.TextField()
    email_type = models.CharField(max_length=50, choices=EMAIL_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    failed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    retry_count = models.PositiveIntegerField(default=0)
    max_retries = models.PositiveIntegerField(default=3)

    # Related task or notification data
    task_id = models.CharField(max_length=255, blank=True, null=True)
    notification_id = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)  # Additional data

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "emails"
        indexes = [
            models.Index(fields=["status", "scheduled_at"]),
            models.Index(fields=["email_type"]),
            models.Index(fields=["task_id"]),
            models.Index(fields=["notification_id"]),
        ]

    def __str__(self):
        return f"Email to {self.recipient} - {self.subject}"

    def mark_as_sent(self):
        """Mark email as sent"""
        self.status = "sent"
        self.sent_at = timezone.now()
        self.save()

    def mark_as_failed(self, error_message):
        """Mark email as failed"""
        self.status = "failed"
        self.failed_at = timezone.now()
        self.error_message = error_message
        self.retry_count += 1
        self.save()

    def can_retry(self):
        """Check if email can be retried"""
        return self.retry_count < self.max_retries and self.status == "failed"


class ScheduledTask(models.Model):
    """Model for storing scheduled tasks that trigger emails"""

    TASK_TYPES = [
        ("meeting_reminder", "Meeting Reminder"),
        ("application_deadline", "Application Deadline"),
        ("task_due", "Task Due"),
        ("interview_reminder", "Interview Reminder"),
    ]

    task_id = models.CharField(max_length=255, unique=True)
    task_type = models.CharField(max_length=50, choices=TASK_TYPES)
    scheduled_at = models.DateTimeField()
    is_processed = models.BooleanField(default=False)

    # Email details
    recipient_email = models.EmailField()
    email_template = models.ForeignKey(
        EmailTemplate, on_delete=models.CASCADE, null=True, blank=True
    )
    email_data = models.JSONField(blank=True, null=True)  # Data to populate template

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "scheduled_tasks"
        indexes = [
            models.Index(fields=["scheduled_at", "is_processed"]),
            models.Index(fields=["task_type"]),
        ]

    def __str__(self):
        return f"Task {self.task_id} - {self.task_type}"

    def mark_as_processed(self):
        """Mark task as processed"""
        self.is_processed = True
        self.processed_at = timezone.now()
        self.save()


class EmailQueue(models.Model):
    """Queue model for managing email sending queue via RabbitMQ"""

    PRIORITY_CHOICES = [
        (1, "Low"),
        (2, "Normal"),
        (3, "High"),
        (4, "Critical"),
    ]

    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=2)
    queue_name = models.CharField(max_length=100, default="email_queue")
    is_queued = models.BooleanField(default=False)
    queued_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "email_queue"

    def __str__(self):
        return f"Queue for {self.email.recipient}"
