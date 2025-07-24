from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    """
    Model representing tasks that can be assigned to users at workflow steps
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    task_id = models.AutoField(primary_key=True)
    step_id = models.IntegerField(help_text="Foreign key reference to workflow step")
    assignee_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_tasks"
    )
    description = models.TextField()
    due_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['due_date', '-task_id']

    def __str__(self):
        return f"Task {self.task_id} - {self.description[:50]} ({self.status})"

    @property
    def is_completed(self):
        return self.status == "completed"
