"""
Integration example showing how to trigger notifications and tasks
when a job application moves through workflow steps.

This would typically be called from the application service when
job applications change status.
"""

from django.utils import timezone
from apps.api.tasks import trigger_workflow_notifications, create_task_for_step
from apps.api.models.notification import Notification
from apps.api.models.task import Task
from django.contrib.auth.models import User


def handle_application_status_change(
    application_id, old_step_id, new_step_id, user_context=None
):
    """
    Handle application moving from one workflow step to another.

    Args:
        application_id: ID of the job application
        old_step_id: Previous workflow step ID
        new_step_id: New workflow step ID
        user_context: Dict containing user info (email, user_id, etc.)
    """

    # Trigger notifications for the new step
    context = {
        "application_id": application_id,
        "old_step": old_step_id,
        "new_step": new_step_id,
        "recipient_email": user_context.get("email") if user_context else None,
        "user_id": user_context.get("user_id") if user_context else None,
    }

    # Trigger workflow notifications asynchronously
    trigger_workflow_notifications.delay(new_step_id, context)

    # Example: Create specific tasks based on workflow step
    if new_step_id == 1:  # Application received
        # Create task for HR to review application
        hr_users = User.objects.filter(groups__name="HR")
        if hr_users.exists():
            create_task_for_step.delay(
                step_id=new_step_id,
                assignee_id=hr_users.first().id,
                description=f"Review application {application_id} - Initial screening",
                context={"notify_assignee": True},
            )

    elif new_step_id == 2:  # Phone screening
        # Create task for interviewer
        interviewer_id = user_context.get("interviewer_id") if user_context else None
        if interviewer_id:
            create_task_for_step.delay(
                step_id=new_step_id,
                assignee_id=interviewer_id,
                description=f"Conduct phone screening for application {application_id}",
                context={"notify_assignee": True},
            )

    elif new_step_id == 3:  # Technical interview
        # Create task for technical team lead
        tech_leads = User.objects.filter(groups__name="Tech Lead")
        if tech_leads.exists():
            create_task_for_step.delay(
                step_id=new_step_id,
                assignee_id=tech_leads.first().id,
                description=f"Schedule technical interview for application {application_id}",
                context={"notify_assignee": True},
            )

    elif new_step_id == 4:  # Final decision
        # Create task for hiring manager
        managers = User.objects.filter(groups__name="Hiring Manager")
        if managers.exists():
            create_task_for_step.delay(
                step_id=new_step_id,
                assignee_id=managers.first().id,
                description=f"Make final decision on application {application_id}",
                context={"notify_assignee": True},
            )


def setup_default_notifications():
    """
    Create default notifications for common workflow steps.
    This would typically be run during initial setup.
    """

    default_notifications = [
        {
            "step_id": 1,
            "channel": "email",
            "template_name": "application_received",
            "trigger_on_entry": True,
        },
        {
            "step_id": 2,
            "channel": "email",
            "template_name": "phone_screening_scheduled",
            "trigger_on_entry": True,
        },
        {
            "step_id": 3,
            "channel": "email",
            "template_name": "technical_interview_invitation",
            "trigger_on_entry": True,
        },
        {
            "step_id": 4,
            "channel": "email",
            "template_name": "decision_pending",
            "trigger_on_entry": True,
        },
        {
            "step_id": 5,
            "channel": "email",
            "template_name": "offer_extended",
            "trigger_on_entry": True,
        },
        {
            "step_id": 6,
            "channel": "email",
            "template_name": "application_rejected",
            "trigger_on_entry": True,
        },
    ]

    for notification_data in default_notifications:
        Notification.objects.get_or_create(
            step_id=notification_data["step_id"],
            channel=notification_data["channel"],
            template_name=notification_data["template_name"],
            defaults={"trigger_on_entry": notification_data["trigger_on_entry"]},
        )

    print(f"Created {len(default_notifications)} default notifications")


def get_workflow_statistics():
    """
    Get statistics about current workflow state.
    """
    from django.db.models import Count

    # Task statistics
    task_stats = Task.objects.values("status").annotate(count=Count("status"))
    notification_stats = Notification.objects.values("channel").annotate(
        count=Count("channel")
    )

    return {
        "task_statistics": list(task_stats),
        "notification_statistics": list(notification_stats),
        "total_tasks": Task.objects.count(),
        "total_notifications": Notification.objects.count(),
        "pending_tasks": Task.objects.filter(status="pending").count(),
        "overdue_tasks": Task.objects.filter(
            due_date__lt=timezone.now(), status__in=["pending", "in_progress"]
        ).count()
        if "timezone" in globals()
        else 0,
    }


# Example API integration for external services
class WorkflowIntegrationAPI:
    """
    API wrapper for external services to integrate with the notification system.
    """

    @staticmethod
    def trigger_step_notifications(step_id, context_data):
        """
        Trigger notifications for a specific workflow step.

        Args:
            step_id: The workflow step ID
            context_data: Dictionary with context for notifications

        Returns:
            Task ID of the triggered notification job
        """
        result = trigger_workflow_notifications.delay(step_id, context_data)
        return result.id

    @staticmethod
    def create_workflow_task(step_id, assignee_id, description, due_date=None):
        """
        Create a task for a workflow step.

        Args:
            step_id: The workflow step ID
            assignee_id: User ID to assign the task to
            description: Task description
            due_date: Optional due date

        Returns:
            Task ID of the created task job
        """
        result = create_task_for_step.delay(
            step_id=step_id,
            assignee_id=assignee_id,
            description=description,
            due_date=due_date,
        )
        return result.id

    @staticmethod
    def get_step_notifications(step_id):
        """
        Get all notifications configured for a workflow step.

        Args:
            step_id: The workflow step ID

        Returns:
            List of notification configurations
        """
        notifications = Notification.objects.filter(step_id=step_id)
        return [
            {
                "notification_id": n.notification_id,
                "channel": n.channel,
                "template_name": n.template_name,
                "trigger_on_entry": n.trigger_on_entry,
            }
            for n in notifications
        ]

    @staticmethod
    def get_user_tasks(user_id, status=None):
        """
        Get tasks assigned to a specific user.

        Args:
            user_id: The user ID
            status: Optional status filter

        Returns:
            List of user tasks
        """
        tasks = Task.objects.filter(assignee_id=user_id)
        if status:
            tasks = tasks.filter(status=status)

        return [
            {
                "task_id": t.task_id,
                "step_id": t.step_id,
                "description": t.description,
                "status": t.status,
                "due_date": t.due_date,
                "created_at": t.created_at,
            }
            for t in tasks
        ]
