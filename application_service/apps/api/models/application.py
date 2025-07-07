from django.db import models
from .job import Job
from .candidate import Candidate


class Application(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('Interview', 'Interview'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired'),
        ('On Hold', 'On Hold'),
        ('Withdrawn', 'Withdrawn'),
    ]

    application_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    current_stage = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'applications'
        ordering = ['-applied_at']
        unique_together = ['job', 'candidate']

    def __str__(self):
        return f"{self.candidate.full_name} - {self.job.title}"
