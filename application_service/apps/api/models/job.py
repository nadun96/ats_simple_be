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
    WORK_TIME_CHOICES = [
        ('full-time', 'Full-time'),
        ('part-time', 'Part-time'),
        ('contract', 'Contract Basis'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('internal_distribution', 'Internal Distribution'),
        ('restricted', 'Restricted'),
    ]
    
    QUALIFICATION_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('junior', 'Junior Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('lead', 'Lead Level'),
        ('executive', 'Executive Level'),
    ]

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
    contract_length = models.PositiveIntegerField(help_text="Contract length in days", null=True, blank=True)
    work_time = models.CharField(max_length=50, choices=WORK_TIME_CHOICES, default='full-time')
    candidate_profile = models.TextField(help_text="Expected qualifications, experience, and candidate profile", blank=True)
    visibility_of_job = models.CharField(max_length=50, choices=VISIBILITY_CHOICES, default='public')
    department = models.CharField(max_length=200, blank=True)
    qualification_level = models.CharField(max_length=50, choices=QUALIFICATION_LEVEL_CHOICES, default='mid')

    class Meta:
        db_table = 'job_descriptions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"
