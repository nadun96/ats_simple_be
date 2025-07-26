from django.db import models
from .job import Job


class Workflow(models.Model):
    workflow_id = models.AutoField(primary_key=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="workflow")
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflows"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Workflow: {self.name} for {self.job.title}"
