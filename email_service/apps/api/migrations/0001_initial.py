# Generated manually for initial schema

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmailTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255, unique=True)),
                (
                    "template_type",
                    models.CharField(
                        choices=[
                            ("notification", "Notification"),
                            ("task_reminder", "Task Reminder"),
                            ("application_status", "Application Status"),
                            ("meeting_reminder", "Meeting Reminder"),
                            ("confirmation", "Confirmation"),
                        ],
                        max_length=50,
                    ),
                ),
                ("subject", models.CharField(max_length=255)),
                ("body_html", models.TextField()),
                ("body_text", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "email_templates",
            },
        ),
        migrations.CreateModel(
            name="Email",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("sender", models.EmailField(max_length=254)),
                ("recipient", models.EmailField(max_length=254)),
                ("cc", models.TextField(blank=True, null=True)),
                ("bcc", models.TextField(blank=True, null=True)),
                ("subject", models.CharField(max_length=255)),
                ("body_html", models.TextField()),
                ("body_text", models.TextField()),
                (
                    "email_type",
                    models.CharField(
                        choices=[
                            ("notification", "Notification"),
                            ("task_reminder", "Task Reminder"),
                            ("application_status", "Application Status"),
                            ("meeting_reminder", "Meeting Reminder"),
                            ("confirmation", "Confirmation"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("sent", "Sent"),
                            ("failed", "Failed"),
                            ("scheduled", "Scheduled"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("scheduled_at", models.DateTimeField(blank=True, null=True)),
                ("sent_at", models.DateTimeField(blank=True, null=True)),
                ("failed_at", models.DateTimeField(blank=True, null=True)),
                ("error_message", models.TextField(blank=True, null=True)),
                ("retry_count", models.PositiveIntegerField(default=0)),
                ("max_retries", models.PositiveIntegerField(default=3)),
                ("task_id", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "notification_id",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("metadata", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "emails",
            },
        ),
        migrations.CreateModel(
            name="ScheduledTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task_id", models.CharField(max_length=255, unique=True)),
                (
                    "task_type",
                    models.CharField(
                        choices=[
                            ("meeting_reminder", "Meeting Reminder"),
                            ("application_deadline", "Application Deadline"),
                            ("task_due", "Task Due"),
                            ("interview_reminder", "Interview Reminder"),
                        ],
                        max_length=50,
                    ),
                ),
                ("scheduled_at", models.DateTimeField()),
                ("is_processed", models.BooleanField(default=False)),
                ("recipient_email", models.EmailField(max_length=254)),
                ("email_data", models.JSONField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("processed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "email_template",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="api.emailtemplate",
                    ),
                ),
            ],
            options={
                "db_table": "scheduled_tasks",
            },
        ),
        migrations.CreateModel(
            name="EmailQueue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "priority",
                    models.PositiveIntegerField(
                        choices=[
                            (1, "Low"),
                            (2, "Normal"),
                            (3, "High"),
                            (4, "Critical"),
                        ],
                        default=2,
                    ),
                ),
                ("queue_name", models.CharField(default="email_queue", max_length=100)),
                ("is_queued", models.BooleanField(default=False)),
                ("queued_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "email",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.email"
                    ),
                ),
            ],
            options={
                "db_table": "email_queue",
            },
        ),
        migrations.AddIndex(
            model_name="scheduledtask",
            index=models.Index(
                fields=["scheduled_at", "is_processed"],
                name="scheduled_t_schedul_bb0b8c_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="scheduledtask",
            index=models.Index(
                fields=["task_type"], name="scheduled_t_task_ty_3bc0bd_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="email",
            index=models.Index(
                fields=["status", "scheduled_at"], name="emails_status_8e2e4a_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="email",
            index=models.Index(fields=["email_type"], name="emails_email_t_a9d5af_idx"),
        ),
        migrations.AddIndex(
            model_name="email",
            index=models.Index(fields=["task_id"], name="emails_task_id_1a4c63_idx"),
        ),
        migrations.AddIndex(
            model_name="email",
            index=models.Index(
                fields=["notification_id"], name="emails_notific_71da88_idx"
            ),
        ),
    ]
