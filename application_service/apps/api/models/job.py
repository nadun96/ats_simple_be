from django.db import models
from django.contrib.auth.models import User


class Society(models.Model):
    """Company/Society information"""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    banner = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "societies"
        verbose_name_plural = "Societies"

    def __str__(self):
        return self.name or "Unnamed Society"


class Job(models.Model):
    """Main Job model"""
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Archived", "Archived"),
        ("Draft", "Draft"),
    ]

    URGENCY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    EXPERIENCE_LEVELS = [
        ("Entry-level", "Entry-level"),
        ("Mid-level", "Mid-level"),
        ("Senior", "Senior"),
        ("Lead", "Lead"),
        ("Executive", "Executive"),
    ]

    CONTRACT_TYPES = [
        ("Full-time", "Full-time"),
        ("Part-time", "Part-time"),
        ("Contract", "Contract"),
        ("Freelance", "Freelance"),
        ("Internship", "Internship"),
    ]

    REMOTE_TYPES = [
        ("On-site", "On-site"),
        ("Remote", "Remote"),
        ("Hybrid", "Hybrid"),
    ]

    id = models.AutoField(primary_key=True)
    society = models.ForeignKey(
        Society, on_delete=models.CASCADE, related_name="jobs", blank=True, null=True
    )

    # Job Description fields
    urgency = models.CharField(
        max_length=20, choices=URGENCY_CHOICES, blank=True, null=True
    )
    title = models.CharField(max_length=255, blank=True, null=True)
    is_remote = models.BooleanField(default=False, blank=True, null=True)
    remote_type = models.CharField(
        max_length=20, choices=REMOTE_TYPES, blank=True, null=True
    )
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    type_of_contract = models.CharField(
        max_length=50, choices=CONTRACT_TYPES, blank=True, null=True
    )
    contract_duration_length = models.IntegerField(blank=True, null=True)
    contract_duration_unit = models.CharField(max_length=20, blank=True, null=True)
    experience_level = models.CharField(
        max_length=50, choices=EXPERIENCE_LEVELS, blank=True, null=True
    )
    language = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    salary_min = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    salary_max = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    salary_currency = models.CharField(
        max_length=10, blank=True, null=True, default="USD"
    )
    level = models.CharField(max_length=50, blank=True, null=True)
    post_text_html = models.TextField(blank=True, null=True)
    post_text_markdown = models.TextField(blank=True, null=True)
    post_text_plain = models.TextField(blank=True, null=True)
    application_link = models.URLField(blank=True, null=True)
    responsibilities = models.JSONField(default=list, blank=True, null=True)
    qualifications = models.JSONField(default=list, blank=True, null=True)
    benefits = models.JSONField(default=list, blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)

    # Settings fields
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    is_draft = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    audience = models.CharField(max_length=50, blank=True, null=True)
    visibility = models.CharField(
        max_length=50, blank=True, null=True, default="Public"
    )
    application_process = models.TextField(blank=True, null=True)

    # Tags
    tags = models.JSONField(default=list, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_jobs",
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']

    def __str__(self):
        return self.title or "Untitled Job"


class JobForm(models.Model):
    """Job application form structure"""

    id = models.AutoField(primary_key=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="job_form")
    template_id = models.CharField(max_length=100, blank=True, null=True)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "job_forms"

    def __str__(self):
        return f"Form for {self.job.title}"


class FormField(models.Model):
    """Individual form fields"""

    FIELD_TYPES = [
        ("text", "Text"),
        ("email", "Email"),
        ("number", "Number"),
        ("textarea", "Textarea"),
        ("select", "Select"),
        ("checkbox", "Checkbox"),
        ("radio", "Radio"),
        ("file", "File"),
        ("date", "Date"),
    ]

    id = models.AutoField(primary_key=True)
    job_form = models.ForeignKey(
        JobForm, on_delete=models.CASCADE, related_name="form_fields"
    )
    field_id = models.CharField(max_length=100, blank=True, null=True)
    field_type = models.CharField(
        max_length=50, choices=FIELD_TYPES, blank=True, null=True
    )
    field_name = models.CharField(max_length=255, blank=True, null=True)
    field_description = models.TextField(blank=True, null=True)
    field_placeholder = models.CharField(max_length=255, blank=True, null=True)
    field_options = models.JSONField(default=dict, blank=True, null=True)
    is_required = models.BooleanField(default=False)
    is_multiple = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "form_fields"
        ordering = ["job_form", "order"]

    def __str__(self):
        return f"{self.field_name} ({self.field_type})"


class Team(models.Model):
    """Team associated with job"""

    id = models.AutoField(primary_key=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="team")
    team_template_id = models.CharField(max_length=100, blank=True, null=True)
    team_template_name = models.CharField(max_length=255, blank=True, null=True)
    team_id = models.CharField(max_length=100, blank=True, null=True)
    team_name = models.CharField(max_length=255, blank=True, null=True)
    team_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "teams"

    def __str__(self):
        return self.team_name or "Unnamed Team"


class TeamMember(models.Model):
    """Team members"""

    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="members")
    member_id = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    role = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "team_members"

    def __str__(self):
        return f"{self.name} - {self.role}"


class WorkflowTemplate(models.Model):
    """Workflow template"""

    id = models.AutoField(primary_key=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name="workflow")
    template_id = models.CharField(max_length=100, blank=True, null=True)
    template_name = models.CharField(max_length=255, blank=True, null=True)
    template_description = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflow_templates"

    def __str__(self):
        return self.name or "Unnamed Workflow"


class WorkflowStep(models.Model):
    """Workflow steps"""

    id = models.AutoField(primary_key=True)
    workflow = models.ForeignKey(
        WorkflowTemplate, on_delete=models.CASCADE, related_name="steps"
    )
    step_id = models.CharField(max_length=100, blank=True, null=True)
    step_name = models.CharField(max_length=255, blank=True, null=True)
    step_description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_required = models.BooleanField(default=True)
    tags = models.JSONField(default=list, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflow_steps"
        ordering = ["workflow", "order"]

    def __str__(self):
        return self.step_name or "Unnamed Step"


class WorkflowAction(models.Model):
    """Actions within workflow steps"""

    ACTION_TYPES = [
        ("email", "Email"),
        ("notification", "Notification"),
        ("task", "Task"),
        ("meeting", "Meeting"),
    ]

    id = models.AutoField(primary_key=True)
    step = models.ForeignKey(
        WorkflowStep, on_delete=models.CASCADE, related_name="actions"
    )
    action_id = models.CharField(max_length=100, blank=True, null=True)
    action_name = models.CharField(max_length=255, blank=True, null=True)
    action_type = models.CharField(
        max_length=50, choices=ACTION_TYPES, blank=True, null=True
    )
    action_description = models.TextField(blank=True, null=True)
    email_template = models.CharField(max_length=100, blank=True, null=True)
    action_details = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflow_actions"

    def __str__(self):
        return self.action_name or "Unnamed Action"


class WorkflowTask(models.Model):
    """Tasks within workflow steps"""

    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    id = models.AutoField(primary_key=True)
    step = models.ForeignKey(
        WorkflowStep, on_delete=models.CASCADE, related_name="tasks"
    )
    task_id = models.CharField(max_length=100, blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    task_description = models.TextField(blank=True, null=True)
    assignee_member_id = models.CharField(max_length=100, blank=True, null=True)
    assignee_name = models.CharField(max_length=255, blank=True, null=True)
    assignee_role = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)
    schedule = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, blank=True, null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "workflow_tasks"

    def __str__(self):
        return self.task_name or "Unnamed Task"


class TaskComment(models.Model):
    """Comments on tasks"""

    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        WorkflowTask, on_delete=models.CASCADE, related_name="comments"
    )
    comment_id = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_comments"
        ordering = ["timestamp"]

    def __str__(self):
        return f"Comment by {self.author}"


class StepLink(models.Model):
    """Links within workflow steps"""

    LINK_TYPES = [
        ("meeting", "Meeting"),
        ("form", "Form"),
        ("document", "Document"),
        ("external", "External"),
    ]

    id = models.AutoField(primary_key=True)
    step = models.ForeignKey(
        WorkflowStep, on_delete=models.CASCADE, related_name="links"
    )
    type = models.CharField(max_length=50, choices=LINK_TYPES, blank=True, null=True)
    link_id = models.CharField(max_length=100, blank=True, null=True)
    link_name = models.CharField(max_length=255, blank=True, null=True)
    link_url = models.URLField(blank=True, null=True)
    link_description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    expires_on = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "step_links"

    def __str__(self):
        return self.link_name or "Unnamed Link"


class JobSite(models.Model):
    """Sites where job is posted"""

    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Inactive", "Inactive"),
        ("Draft", "Draft"),
        ("Archived", "Archived"),
    ]

    VISIBILITY_CHOICES = [
        ("Public", "Public"),
        ("Private", "Private"),
        ("Internal", "Internal"),
    ]

    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="sites")
    site_id = models.CharField(max_length=100, blank=True, null=True)
    site_name = models.CharField(max_length=255, blank=True, null=True)
    site_description = models.TextField(blank=True, null=True)
    site_url = models.URLField(blank=True, null=True)
    job_link = models.URLField(blank=True, null=True)
    posted_on = models.DateTimeField(blank=True, null=True)
    is_live = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    tags = models.JSONField(default=list, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Draft")
    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default="Public"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "job_sites"

    def __str__(self):
        return self.site_name or "Unnamed Site"


# Legacy models for backward compatibility
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
