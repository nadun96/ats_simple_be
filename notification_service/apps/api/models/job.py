from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Archived', 'Archived'),
    ]

    job_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class PipelineStage(models.Model):
    stage_id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='pipeline_stages')
    name = models.CharField(max_length=100)  # e.g., Screening, Interview, Offer
    order = models.PositiveIntegerField()

    class Meta:
        db_table = 'pipeline_stages'
        ordering = ['job', 'order']
        unique_together = ['job', 'order']

    def __str__(self):
        return f"{self.job.title} - {self.name}"


class JobDescription(models.Model):
    company_name = models.CharField(max_length=255)
    url_of_site = models.URLField()
    company_description = models.TextField()
    company_logo = models.URLField(blank=True)
    job_title = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    isRemote = models.BooleanField()
    type_of_contract = models.CharField(max_length=100)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    banner_image = models.ImageField(upload_to='banners/', blank=True, null=True)

    class Meta:
        db_table = 'job_descriptions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"
