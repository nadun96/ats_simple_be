from django.db import models


class Notification(models.Model):
    """
    Model representing notifications that can be triggered at workflow steps
    """

    CHANNEL_CHOICES = [
        ("email", "Email"),
        ("sms", "SMS"),
        ("push", "Push Notification"),
        ("in_app", "In-App Notification"),
    ]

    notification_id = models.AutoField(primary_key=True)
    step_id = models.IntegerField(help_text="Foreign key reference to workflow step")
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default="email")
    template_name = models.CharField(
        max_length=255, help_text="Name of the notification template"
    )
    trigger_on_entry = models.BooleanField(
        default=True,
        help_text="Whether to trigger notification when entering this step",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notifications"
        ordering = ["step_id", "-created_at"]

    def __str__(self):
        return f"Notification {self.notification_id} - {self.template_name} ({self.channel})"
