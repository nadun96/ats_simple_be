from django.db import models


class WorkflowTemplate(models.Model):
    """
    Template model for creating reusable workflows.
    These templates can be used to create workflows for different jobs.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "workflow_templates"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Workflow Template: {self.name}"
