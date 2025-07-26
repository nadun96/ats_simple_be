from django.db import models
from .workflowtemplate import WorkflowTemplate


class WorkflowStageTemplate(models.Model):
    """
    Template model for workflow stages/steps.
    These define the standard stages that can be used in workflow templates.
    """

    STAGE_TYPE_CHOICES = [
        ("screening", "Screening"),
        ("interview", "Interview"),
        ("assessment", "Assessment"),
        ("reference_check", "Reference Check"),
        ("offer", "Offer"),
        ("onboarding", "Onboarding"),
        ("custom", "Custom"),
    ]

    id = models.AutoField(primary_key=True)
    template = models.ForeignKey(
        WorkflowTemplate, on_delete=models.CASCADE, related_name="stages"
    )
    order_index = models.PositiveIntegerField()
    stage_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    stage_type = models.CharField(max_length=50, choices=STAGE_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflow_stage_templates"
        ordering = ["template", "order_index"]
        unique_together = ["template", "order_index"]

    def __str__(self):
        return f"{self.template.name} - Stage {self.order_index}: {self.stage_name}"
