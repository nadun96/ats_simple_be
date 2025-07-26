from django.db import models
from .workflow import Workflow


class WorkflowStep(models.Model):
    STEP_TYPE_CHOICES = [
        ("screening", "Screening"),
        ("interview", "Interview"),
        ("assessment", "Assessment"),
        ("reference_check", "Reference Check"),
        ("offer", "Offer"),
        ("onboarding", "Onboarding"),
        ("custom", "Custom"),
    ]

    step_id = models.AutoField(primary_key=True)
    workflow = models.ForeignKey(
        Workflow, on_delete=models.CASCADE, related_name="steps"
    )
    step_order = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    step_type = models.CharField(max_length=50, choices=STEP_TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflow_steps"
        ordering = ["workflow", "step_order"]
        unique_together = ["workflow", "step_order"]

    def __str__(self):
        return f"{self.workflow.name} - Step {self.step_order}: {self.name}"
