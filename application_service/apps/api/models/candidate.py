from django.db import models


class Candidate(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    resume_file_path = models.FileField(upload_to="resumes/", blank=True, null=True)
    cover_letter = models.TextField(blank=True, null=True)
    parsed_cv_data = models.JSONField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    education = models.JSONField(default=list, blank=True, null=True)
    work_experience = models.JSONField(default=list, blank=True, null=True)
    certifications = models.JSONField(default=list, blank=True, null=True)
    languages = models.JSONField(default=list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'candidates'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
