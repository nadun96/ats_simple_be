from rest_framework import serializers
from .models.job import JobDescription
from .models.application import Application
from .models.task import Task
from .models.notification import Notification
from .models.workflow import Workflow
from .models.workflowstep import WorkflowStep
from .models.workflowtemplate import WorkflowTemplate
from .models.workflowstagetemplate import WorkflowStageTemplate
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


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


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model"""

    assignee = UserSerializer(source="assignee_id", read_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    class Meta:
        model = Task
        fields = [
            "task_id",
            "step_id",
            "assignee_id",
            "assignee",
            "description",
            "due_date",
            "status",
            "created_at",
            "updated_at",
            "is_completed",
        ]
        read_only_fields = ["task_id", "created_at", "updated_at", "is_completed"]

    def validate_step_id(self, value):
        """Validate that step_id is positive"""
        if value <= 0:
            raise serializers.ValidationError("Step ID must be positive")
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating tasks"""

    class Meta:
        model = Task
        fields = ["step_id", "assignee_id", "description", "due_date", "status"]


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""

    class Meta:
        model = Notification
        fields = [
            "notification_id",
            "step_id",
            "channel",
            "template_name",
            "trigger_on_entry",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["notification_id", "created_at", "updated_at"]

    def validate_step_id(self, value):
        """Validate that step_id is positive"""
        if value <= 0:
            raise serializers.ValidationError("Step ID must be positive")
        return value

    def validate_template_name(self, value):
        """Validate template name is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Template name cannot be empty")
        return value.strip()


class NotificationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating notifications"""

    class Meta:
        model = Notification
        fields = ["step_id", "channel", "template_name", "trigger_on_entry"]


class WorkflowStepSerializer(serializers.ModelSerializer):
    """Serializer for WorkflowStep model"""

    class Meta:
        model = WorkflowStep
        fields = [
            "step_id",
            "workflow",
            "step_order",
            "name",
            "step_type",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["step_id", "created_at", "updated_at"]

    def validate_step_order(self, value):
        """Validate that step_order is positive"""
        if value <= 0:
            raise serializers.ValidationError("Step order must be positive")
        return value


class WorkflowStepCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating workflow steps"""

    class Meta:
        model = WorkflowStep
        fields = [
            "workflow",
            "step_order",
            "name",
            "step_type",
            "description",
            "is_active",
        ]


class WorkflowSerializer(serializers.ModelSerializer):
    """Serializer for Workflow model"""

    steps = WorkflowStepSerializer(many=True, read_only=True)

    class Meta:
        model = Workflow
        fields = [
            "workflow_id",
            "job",
            "name",
            "created_at",
            "updated_at",
            "steps",
        ]
        read_only_fields = ["workflow_id", "created_at", "updated_at"]


class WorkflowCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating workflows"""

    class Meta:
        model = Workflow
        fields = ["job", "name"]

    def validate_job(self, value):
        """Validate that job doesn't already have a workflow"""
        if hasattr(value, "workflow"):
            raise serializers.ValidationError(
                "This job already has a workflow assigned"
            )
        return value


# ===============================
# WORKFLOW TEMPLATE SERIALIZERS
# ===============================


class WorkflowStageTemplateSerializer(serializers.ModelSerializer):
    """Serializer for WorkflowStageTemplate model"""

    class Meta:
        model = WorkflowStageTemplate
        fields = [
            "id",
            "template",
            "order_index",
            "stage_name",
            "description",
            "stage_type",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_order_index(self, value):
        """Validate that order_index is positive"""
        if value <= 0:
            raise serializers.ValidationError("Order index must be positive")
        return value


class WorkflowStageTemplateCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating workflow stage templates"""

    class Meta:
        model = WorkflowStageTemplate
        fields = [
            "template",
            "order_index",
            "stage_name",
            "description",
            "stage_type",
            "is_active",
        ]


class WorkflowTemplateSerializer(serializers.ModelSerializer):
    """Serializer for WorkflowTemplate model"""

    stages = WorkflowStageTemplateSerializer(many=True, read_only=True)
    stage_count = serializers.SerializerMethodField()

    class Meta:
        model = WorkflowTemplate
        fields = [
            "id",
            "name",
            "description",
            "is_active",
            "created_at",
            "updated_at",
            "stages",
            "stage_count",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "stage_count"]

    def get_stage_count(self, obj):
        """Get the number of stages in this template"""
        return obj.stages.count()


class WorkflowTemplateCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating workflow templates"""

    class Meta:
        model = WorkflowTemplate
        fields = ["name", "description", "is_active"]

    def validate_name(self, value):
        """Validate template name is not empty"""
        if not value.strip():
            raise serializers.ValidationError("Template name cannot be empty")
        return value.strip()


class WorkflowFromTemplateSerializer(serializers.Serializer):
    """Serializer for creating workflows from templates"""

    job_id = serializers.IntegerField()
    template_id = serializers.IntegerField()

    def validate_job_id(self, value):
        """Validate that job exists and doesn't already have a workflow"""
        from .models.job import Job

        try:
            job = Job.objects.get(job_id=value)
        except Job.DoesNotExist:
            raise serializers.ValidationError("Job not found")

        if hasattr(job, "workflow"):
            raise serializers.ValidationError(
                "This job already has a workflow assigned"
            )

        return value

    def validate_template_id(self, value):
        """Validate that template exists and is active"""
        try:
            WorkflowTemplate.objects.get(id=value, is_active=True)
        except WorkflowTemplate.DoesNotExist:
            raise serializers.ValidationError("Active workflow template not found")

        return value

    def create(self, validated_data):
        """Create workflow from template"""
        from .models.job import Job

        job = Job.objects.get(job_id=validated_data["job_id"])
        template = WorkflowTemplate.objects.get(id=validated_data["template_id"])

        return Workflow.create_from_template(job, template)
