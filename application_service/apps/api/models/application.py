from django.db import models
from .job import Job, WorkflowStep, WorkflowTemplate
from .candidate import Candidate


class Application(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("In Review", "In Review"),
        ("Phone Screen", "Phone Screen"),
        ("Interview", "Interview"),
        ("Technical Test", "Technical Test"),
        ("Final Interview", "Final Interview"),
        ("Reference Check", "Reference Check"),
        ("Offer Made", "Offer Made"),
        ("Offer Accepted", "Offer Accepted"),
        ("Rejected", "Rejected"),
        ("Hired", "Hired"),
        ("On Hold", "On Hold"),
        ("Withdrawn", "Withdrawn"),
    ]

    application_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    current_stage = models.ForeignKey(
        WorkflowStep,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="current_applications",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    stage_order = models.PositiveIntegerField(default=0)  # Current position in workflow
    form_answers = models.JSONField(
        default=dict, blank=True, null=True
    )  # Answers to job form
    application_notes = models.TextField(blank=True, null=True)
    internal_notes = models.TextField(blank=True, null=True)
    source = models.CharField(
        max_length=100, blank=True, null=True
    )  # Where application came from
    rating = models.PositiveIntegerField(blank=True, null=True)  # 1-5 rating
    tags = models.JSONField(default=list, blank=True, null=True)
    is_starred = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(
        blank=True, null=True
    )  # Last workflow processing time

    class Meta:
        db_table = 'applications'
        ordering = ['-applied_at']
        unique_together = ['job', 'candidate']

    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.title}"

    def advance_to_next_stage(self):
        """Move application to next workflow stage"""
        if self.job.workflow and self.current_stage:
            next_stages = self.job.workflow.steps.filter(
                order__gt=self.current_stage.order
            ).order_by("order")
            if next_stages.exists():
                self.current_stage = next_stages.first()
                self.stage_order = self.current_stage.order
                self.save()
                return True
        return False

    def move_to_stage(self, stage_id):
        """Move application to specific workflow stage"""
        try:
            stage = WorkflowStep.objects.get(id=stage_id, workflow=self.job.workflow)
            self.current_stage = stage
            self.stage_order = stage.order
            self.save()
            return True
        except WorkflowStep.DoesNotExist:
            return False


class ApplicationStageHistory(models.Model):
    """Track application movement through workflow stages"""

    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="stage_history"
    )
    from_stage = models.ForeignKey(
        WorkflowStep,
        on_delete=models.CASCADE,
        related_name="stage_exits",
        blank=True,
        null=True,
    )
    to_stage = models.ForeignKey(
        WorkflowStep, on_delete=models.CASCADE, related_name="stage_entries"
    )
    changed_by = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "application_stage_history"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.application} moved to {self.to_stage}"


class ApplicationFormAnswer(models.Model):
    """Individual form field answers for applications"""

    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="individual_answers"
    )
    field_id = models.CharField(max_length=100)
    field_name = models.CharField(max_length=255)
    answer_value = models.TextField(blank=True, null=True)
    answer_file = models.FileField(
        upload_to="application_files/", blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "application_form_answers"
        unique_together = ["application", "field_id"]

    def __str__(self):
        return f"{self.application} - {self.field_name}"
