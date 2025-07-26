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

    @classmethod
    def create_from_template(cls, job, template):
        """
        Create a workflow instance from a template.

        Args:
            job: Job instance to associate with the workflow
            template: WorkflowTemplate instance to use as blueprint

        Returns:
            Workflow instance with associated WorkflowStep instances
        """
        # Avoid circular import
        from .workflowstep import WorkflowStep

        # Create workflow instance
        workflow = cls.objects.create(job=job, name=f"{template.name} - {job.title}")

        # Create workflow steps from template stages
        for stage in template.stages.filter(is_active=True).order_by("order_index"):
            WorkflowStep.objects.create(
                workflow=workflow,
                step_order=stage.order_index,
                name=stage.stage_name,
                step_type=stage.stage_type,
                description=stage.description,
                is_active=stage.is_active,
            )

        return workflow
