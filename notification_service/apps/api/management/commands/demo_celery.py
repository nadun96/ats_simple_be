from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.api.models.notification import Notification
from apps.api.models.task import Task
from apps.api.tasks import (
    trigger_workflow_notifications,
    create_task_for_step,
    check_overdue_tasks,
)


class Command(BaseCommand):
    help = "Demo command to test Celery task queue functionality"

    def add_arguments(self, parser):
        parser.add_argument(
            "--action",
            type=str,
            help="Action to perform: create_notification, create_task, trigger_notifications, check_overdue",
            default="create_notification",
        )
        parser.add_argument("--step-id", type=int, help="Workflow step ID", default=1)
        parser.add_argument(
            "--email",
            type=str,
            help="Email address for notification",
            default="test@example.com",
        )

    def handle(self, *args, **options):
        action = options["action"]
        step_id = options["step_id"]
        email = options["email"]

        if action == "create_notification":
            self.create_sample_notification(step_id)
        elif action == "create_task":
            self.create_sample_task(step_id)
        elif action == "trigger_notifications":
            self.trigger_sample_notifications(step_id, email)
        elif action == "check_overdue":
            self.check_overdue_tasks()
        else:
            self.stdout.write(self.style.ERROR(f"Unknown action: {action}"))

    def create_sample_notification(self, step_id):
        """Create a sample notification"""
        notification = Notification.objects.create(
            step_id=step_id,
            channel="email",
            template_name="welcome_notification",
            trigger_on_entry=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Created notification {notification.notification_id} for step {step_id}"
            )
        )

    def create_sample_task(self, step_id):
        """Create a sample task using Celery"""
        # Get or create a user for assignment
        user, created = User.objects.get_or_create(
            username="testuser",
            defaults={
                "email": "testuser@example.com",
                "first_name": "Test",
                "last_name": "User",
            },
        )

        if created:
            user.set_password("testpass123")
            user.save()
            self.stdout.write(f"Created test user: {user.username}")

        # Create task using Celery
        task_result = create_task_for_step.delay(
            step_id=step_id,
            assignee_id=user.id,
            description=f"Sample task for workflow step {step_id}",
            context={"notify_assignee": False},
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Queued task creation for step {step_id}, task ID: {task_result.id}"
            )
        )

    def trigger_sample_notifications(self, step_id, email):
        """Trigger notifications for a workflow step"""
        # Ensure there's a notification for this step
        notification, created = Notification.objects.get_or_create(
            step_id=step_id,
            channel="email",
            defaults={
                "template_name": "step_entry_notification",
                "trigger_on_entry": True,
            },
        )

        if created:
            self.stdout.write(f"Created notification for step {step_id}")

        # Trigger notifications using Celery
        result = trigger_workflow_notifications.delay(
            step_id=step_id,
            context={
                "recipient_email": email,
                "step_name": f"Workflow Step {step_id}",
                "triggered_at": "now",
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Triggered notifications for step {step_id}, task ID: {result.id}"
            )
        )

    def check_overdue_tasks(self):
        """Check for overdue tasks"""
        result = check_overdue_tasks.delay()

        self.stdout.write(
            self.style.SUCCESS(f"Queued overdue task check, task ID: {result.id}")
        )

        # Also show current tasks
        tasks = Task.objects.all()
        self.stdout.write(f"Current tasks in database: {tasks.count()}")
        for task in tasks:
            status_color = (
                self.style.SUCCESS if task.status == "completed" else self.style.WARNING
            )
            self.stdout.write(
                status_color(
                    f"Task {task.task_id}: {task.description[:50]}... (Status: {task.status})"
                )
            )
