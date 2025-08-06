from rest_framework import serializers
from .models import Email, EmailTemplate, ScheduledTask, EmailQueue


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = "__all__"


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"
        read_only_fields = (
            "sent_at",
            "failed_at",
            "retry_count",
            "created_at",
            "updated_at",
        )


class EmailCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating emails"""

    class Meta:
        model = Email
        fields = [
            "sender",
            "recipient",
            "cc",
            "bcc",
            "subject",
            "body_html",
            "body_text",
            "email_type",
            "scheduled_at",
            "task_id",
            "notification_id",
            "metadata",
        ]

    def validate_scheduled_at(self, value):
        """Validate that scheduled_at is in the future"""
        from django.utils import timezone

        if value and value <= timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future")
        return value


class NotificationEmailSerializer(serializers.Serializer):
    """Serializer for immediate notification emails"""

    recipient = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
    email_type = serializers.ChoiceField(choices=Email.EMAIL_TYPES)
    sender = serializers.EmailField(required=False)
    cc = serializers.ListField(
        child=serializers.EmailField(), required=False, allow_empty=True
    )
    bcc = serializers.ListField(
        child=serializers.EmailField(), required=False, allow_empty=True
    )
    notification_id = serializers.CharField(required=False)
    metadata = serializers.JSONField(required=False)


class ScheduledTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledTask
        fields = "__all__"
        read_only_fields = ("is_processed", "processed_at", "created_at")


class ScheduledTaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating scheduled tasks"""

    class Meta:
        model = ScheduledTask
        fields = [
            "task_id",
            "task_type",
            "scheduled_at",
            "recipient_email",
            "email_template",
            "email_data",
        ]

    def validate_scheduled_at(self, value):
        """Validate that scheduled_at is in the future"""
        from django.utils import timezone

        if value <= timezone.now():
            raise serializers.ValidationError("Scheduled time must be in the future")
        return value


class EmailQueueSerializer(serializers.ModelSerializer):
    email = EmailSerializer(read_only=True)

    class Meta:
        model = EmailQueue
        fields = "__all__"
