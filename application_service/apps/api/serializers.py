from rest_framework import serializers
from .models.job import (
    Job,
    JobDescription,
    Society,
    JobForm,
    FormField,
    Team,
    TeamMember,
    WorkflowTemplate,
    WorkflowStep,
    WorkflowAction,
    WorkflowTask,
    TaskComment,
    StepLink,
    JobSite,
)
from .models.application import Application


class SocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Society
        fields = "__all__"


class FormFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormField
        fields = "__all__"


class JobFormSerializer(serializers.ModelSerializer):
    form_fields = FormFieldSerializer(many=True, read_only=True)

    class Meta:
        model = JobForm
        fields = "__all__"


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = "__all__"


class WorkflowTaskSerializer(serializers.ModelSerializer):
    comments = TaskCommentSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowTask
        fields = "__all__"


class WorkflowActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowAction
        fields = "__all__"


class StepLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StepLink
        fields = "__all__"


class WorkflowStepSerializer(serializers.ModelSerializer):
    actions = WorkflowActionSerializer(many=True, read_only=True)
    tasks = WorkflowTaskSerializer(many=True, read_only=True)
    links = StepLinkSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowStep
        fields = "__all__"


class WorkflowTemplateSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowTemplate
        fields = "__all__"


class JobSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSite
        fields = "__all__"


class JobSerializer(serializers.ModelSerializer):
    society = SocietySerializer(required=False)
    job_form = JobFormSerializer(read_only=True)
    team = TeamSerializer(read_only=True)
    workflow = WorkflowTemplateSerializer(read_only=True)
    sites = JobSiteSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = "__all__"

    def create(self, validated_data):
        society_data = validated_data.pop("society", None)

        # Create or get society
        society = None
        if society_data:
            society, created = Society.objects.get_or_create(
                name=society_data.get("name"), defaults=society_data
            )

        # Create job
        job = Job.objects.create(society=society, **validated_data)
        return job


class CompleteJobSerializer(serializers.Serializer):
    """Serializer for the complete job data structure from frontend"""

    # Job description fields
    urgency = serializers.CharField(required=False, allow_blank=True)
    title = serializers.CharField(required=False, allow_blank=True)
    remoteStatus = serializers.DictField(required=False)
    country = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    department = serializers.CharField(required=False, allow_blank=True)
    typeOfContract = serializers.CharField(required=False, allow_blank=True)
    contractDuration = serializers.DictField(required=False)
    experienceLevel = serializers.CharField(required=False, allow_blank=True)
    language = serializers.CharField(required=False, allow_blank=True)
    startDate = serializers.DateField(required=False)
    endDate = serializers.DateField(required=False)
    salary = serializers.DictField(required=False)
    level = serializers.CharField(required=False, allow_blank=True)
    postTextHtml = serializers.CharField(required=False, allow_blank=True)
    postTextMarkdown = serializers.CharField(required=False, allow_blank=True)
    postTextPlain = serializers.CharField(required=False, allow_blank=True)
    applicationLink = serializers.URLField(required=False)
    responsibilities = serializers.ListField(required=False)
    qualifications = serializers.ListField(required=False)
    benefits = serializers.ListField(required=False)
    applicationDeadline = serializers.DateField(required=False)

    # Settings fields
    settings = serializers.DictField(required=False)

    # Society fields
    society = serializers.DictField(required=False)

    # Tag fields
    tag = serializers.DictField(required=False)

    # JobForm fields
    JobForm = serializers.DictField(required=False)

    # Team fields
    Team = serializers.DictField(required=False)

    # WorkFlow fields
    WorkFlow = serializers.DictField(required=False)

    # Sites fields
    sites = serializers.ListField(required=False)

    def create(self, validated_data):
        # Extract nested data
        society_data = validated_data.pop("society", {})
        job_form_data = validated_data.pop("JobForm", {})
        team_data = validated_data.pop("Team", {})
        workflow_data = validated_data.pop("WorkFlow", {})
        sites_data = validated_data.pop("sites", [])
        settings_data = validated_data.pop("settings", {})
        tag_data = validated_data.pop("tag", {})
        remote_status = validated_data.pop("remoteStatus", {})
        contract_duration = validated_data.pop("contractDuration", {})
        salary_data = validated_data.pop("salary", {})

        # Create society
        society = None
        if society_data:
            society, created = Society.objects.get_or_create(
                name=society_data.get("name"),
                defaults={
                    "type": society_data.get("type"),
                    "industry": society_data.get("industry"),
                    "size": society_data.get("size"),
                    "logo": society_data.get("logo"),
                    "banner": society_data.get("banner"),
                    "email": society_data.get("contact", {}).get("email"),
                    "phone": society_data.get("contact", {}).get("phone"),
                    "address": society_data.get("contact", {}).get("address"),
                    "linkedin": society_data.get("contact", {})
                    .get("social", {})
                    .get("linkedin"),
                    "twitter": society_data.get("contact", {})
                    .get("social", {})
                    .get("twitter"),
                    "facebook": society_data.get("contact", {})
                    .get("social", {})
                    .get("facebook"),
                    "website": society_data.get("website"),
                    "description": society_data.get("description"),
                },
            )

        # Prepare job data
        job_data = {
            "society": society,
            "title": validated_data.get("title"),
            "urgency": validated_data.get("urgency"),
            "country": validated_data.get("country"),
            "city": validated_data.get("city"),
            "department": validated_data.get("department"),
            "type_of_contract": validated_data.get("typeOfContract"),
            "experience_level": validated_data.get("experienceLevel"),
            "language": validated_data.get("language"),
            "start_date": validated_data.get("startDate"),
            "end_date": validated_data.get("endDate"),
            "level": validated_data.get("level"),
            "post_text_html": validated_data.get("postTextHtml"),
            "post_text_markdown": validated_data.get("postTextMarkdown"),
            "post_text_plain": validated_data.get("postTextPlain"),
            "application_link": validated_data.get("applicationLink"),
            "responsibilities": validated_data.get("responsibilities", []),
            "qualifications": validated_data.get("qualifications", []),
            "benefits": validated_data.get("benefits", []),
            "application_deadline": validated_data.get("applicationDeadline"),
        }

        # Handle remote status
        if remote_status:
            job_data["is_remote"] = remote_status.get("isRemote", False)
            job_data["remote_type"] = remote_status.get(
                "remoteType", remote_status.get("type")
            )

        # Handle contract duration
        if contract_duration:
            job_data["contract_duration_length"] = contract_duration.get("length")
            job_data["contract_duration_unit"] = contract_duration.get("unit")

        # Handle salary
        if salary_data:
            job_data["salary_min"] = salary_data.get("min")
            job_data["salary_max"] = salary_data.get("max")
            job_data["salary_currency"] = salary_data.get("currency", "USD")

        # Handle settings
        if settings_data:
            job_data["is_active"] = settings_data.get("isActive", True)
            job_data["is_featured"] = settings_data.get("isFeatured", False)
            job_data["is_public"] = settings_data.get("isPublic", True)
            job_data["is_draft"] = settings_data.get("isDraft", False)
            job_data["is_archived"] = settings_data.get("isArchived", False)
            job_data["audience"] = settings_data.get(
                "auduiance"
            )  # Note: typo in original data
            job_data["visibility"] = settings_data.get("visibility", "Public")
            job_data["application_process"] = settings_data.get("applicationProcess")

        # Handle tags
        if tag_data:
            job_data["tags"] = tag_data.get("tags", [])

        # Create job
        job = Job.objects.create(**job_data)

        # Create job form
        if job_form_data:
            job_form = JobForm.objects.create(
                job=job,
                template_id=job_form_data.get("templateId"),
                template_name=job_form_data.get("templateName"),
                template_description=job_form_data.get("templateDescription"),
                title=job_form_data.get("title"),
            )

            # Create form fields
            for field_data in job_form_data.get("formFields", []):
                FormField.objects.create(
                    job_form=job_form,
                    field_id=field_data.get("fieldId"),
                    field_type=field_data.get("fieldType"),
                    field_name=field_data.get("fieldName"),
                    field_description=field_data.get("fieldDescription"),
                    field_placeholder=field_data.get("fieldPlaceholder"),
                    field_options=field_data.get("fieldOptions", {}),
                    is_required=field_data.get("isRequired", False),
                    is_multiple=field_data.get("isMultiple", False),
                    is_active=field_data.get("isActive", True),
                )

        # Create team
        if team_data:
            team = Team.objects.create(
                job=job,
                team_template_id=team_data.get("teamTemplateId"),
                team_template_name=team_data.get("teamTemplateName"),
                team_id=team_data.get("teamId"),
                team_name=team_data.get("teamName"),
                team_description=team_data.get("teamDescription"),
            )

            # Create team members
            for member_data in team_data.get("members", []):
                TeamMember.objects.create(
                    team=team,
                    member_id=member_data.get("memberId"),
                    name=member_data.get("name"),
                    role=member_data.get("role"),
                    email=member_data.get("email"),
                )

        # Create workflow
        if workflow_data and "template" in workflow_data:
            template_data = workflow_data["template"]
            workflow = WorkflowTemplate.objects.create(
                job=job,
                template_id=template_data.get("templateId"),
                template_name=template_data.get("templateName"),
                template_description=template_data.get("templateDescription"),
                name=template_data.get("name"),
                description=template_data.get("description"),
            )

            # Create workflow steps
            for step_data in template_data.get("steps", []):
                step = WorkflowStep.objects.create(
                    workflow=workflow,
                    step_id=step_data.get("stepId"),
                    step_name=step_data.get("stepName"),
                    step_description=step_data.get("stepDescription"),
                    order=step_data.get("order", 0),
                    is_active=step_data.get("isActive", True),
                    is_required=step_data.get("isRequired", True),
                    tags=step_data.get("tag", {}).get("tags", []),
                )

                # Create actions
                for action_data in step_data.get("actions", []):
                    WorkflowAction.objects.create(
                        step=step,
                        action_id=action_data.get("actionId"),
                        action_name=action_data.get("actionName"),
                        action_type=action_data.get("actionType"),
                        action_description=action_data.get("actionDescription"),
                        email_template=action_data.get("emailTemplate"),
                        action_details=action_data.get("actionDetails", {}),
                    )

                # Create tasks
                for task_data in step_data.get("tasks", []):
                    task = WorkflowTask.objects.create(
                        step=step,
                        task_id=task_data.get("taskId"),
                        task_name=task_data.get("taskName"),
                        task_description=task_data.get("taskDescription"),
                        assignee_member_id=task_data.get("assignee", {}).get(
                            "memberId"
                        ),
                        assignee_name=task_data.get("assignee", {}).get("name"),
                        assignee_role=task_data.get("assignee", {}).get("role"),
                        due_date=task_data.get("dueDate"),
                        schedule=task_data.get("schedule"),
                        priority=task_data.get("priority"),
                        status=task_data.get("status", "Pending"),
                    )

                    # Create task comments
                    for comment_data in task_data.get("comments", []):
                        TaskComment.objects.create(
                            task=task,
                            comment_id=comment_data.get("commentId"),
                            author=comment_data.get("author"),
                            content=comment_data.get("content"),
                            timestamp=comment_data.get("timestamp"),
                        )

                # Create links
                for link_data in step_data.get("links", []):
                    StepLink.objects.create(
                        step=step,
                        type=link_data.get("type"),
                        link_id=link_data.get("linkId"),
                        link_name=link_data.get("linkName"),
                        link_url=link_data.get("linkUrl"),
                        link_description=link_data.get("linkDescription"),
                        is_active=link_data.get("isActive", True),
                        expires_on=link_data.get("expiresOn"),
                    )

        # Create job sites
        for site_data in sites_data:
            JobSite.objects.create(
                job=job,
                site_id=site_data.get("siteId"),
                site_name=site_data.get("siteName"),
                site_description=site_data.get("siteDescription"),
                site_url=site_data.get("siteUrl"),
                job_link=site_data.get("jobLink"),
                posted_on=site_data.get("postedOn"),
                is_live=site_data.get("isLive", False),
                is_draft=site_data.get("isDraft", True),
                is_archived=site_data.get("isArchived", False),
                tags=site_data.get("tags", []),
                status=site_data.get("status", "Draft"),
                visibility=site_data.get("visibility", "Public"),
            )

        return job


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = [
            'company_name',
            'url_of_site',
            'company_description',
            'company_logo',
            'job_title',
            'country',
            'city',
            'isRemote',
            'type_of_contract',
            'job_description',
            'created_at',
            'banner_image',
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'application_id',
            'job',
            'candidate',
            'current_stage',
            'status',
            'applied_at',
        ]
