from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from .serializers import (
    JobDescriptionSerializer,
    ApplicationSerializer,
    TaskSerializer,
    TaskCreateSerializer,
    NotificationSerializer,
    NotificationCreateSerializer,
    WorkflowSerializer,
    WorkflowCreateSerializer,
    WorkflowStepSerializer,
    WorkflowStepCreateSerializer,
    WorkflowTemplateSerializer,
    WorkflowTemplateCreateSerializer,
    WorkflowStageTemplateSerializer,
    WorkflowStageTemplateCreateSerializer,
    WorkflowFromTemplateSerializer,
)
from .models.application import Application
from .models.job import JobDescription
from .models.task import Task
from .models.notification import Notification
from .models.workflow import Workflow
from .models.workflowstep import WorkflowStep
from .models.workflowtemplate import WorkflowTemplate
from .models.workflowstagetemplate import WorkflowStageTemplate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser, FormParser


class JobDescriptionView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Create a new job description.",
        request_body=JobDescriptionSerializer,
        responses={201: JobDescriptionSerializer},
    )
    def post(self, request):
        serializer = JobDescriptionSerializer(data=request.data)
        if serializer.is_valid():
            job_desc = serializer.save()
            return Response(JobDescriptionSerializer(job_desc).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationListView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]


class JobDescriptionListView(ListAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
    permission_classes = [AllowAny]


# Task Views
class TaskListCreateView(ListCreateAPIView):
    """
    List all tasks or create a new task.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve list of all tasks",
        responses={200: TaskSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                "status",
                openapi.IN_QUERY,
                description="Filter tasks by status",
                type=openapi.TYPE_STRING,
                enum=["pending", "in_progress", "completed", "cancelled"],
            ),
            openapi.Parameter(
                "assignee_id",
                openapi.IN_QUERY,
                description="Filter tasks by assignee ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "step_id",
                openapi.IN_QUERY,
                description="Filter tasks by workflow step ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter by status
        status_filter = request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by assignee
        assignee_id = request.query_params.get("assignee_id")
        if assignee_id:
            queryset = queryset.filter(assignee_id=assignee_id)

        # Filter by step_id
        step_id = request.query_params.get("step_id")
        if step_id:
            queryset = queryset.filter(step_id=step_id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new task",
        request_body=TaskCreateSerializer,
        responses={201: TaskSerializer, 400: "Bad Request - Invalid data"},
    )
    def post(self, request, *args, **kwargs):
        # Use TaskCreateSerializer for validation
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            # Return full task data using TaskSerializer
            response_serializer = TaskSerializer(task)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a task instance.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    lookup_field = "task_id"

    @swagger_auto_schema(
        operation_description="Retrieve a specific task",
        responses={200: TaskSerializer, 404: "Task not found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific task",
        request_body=TaskSerializer,
        responses={
            200: TaskSerializer,
            400: "Bad Request - Invalid data",
            404: "Task not found",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific task",
        request_body=TaskSerializer,
        responses={
            200: TaskSerializer,
            400: "Bad Request - Invalid data",
            404: "Task not found",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific task",
        responses={204: "Task deleted successfully", 404: "Task not found"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# Notification Views
class NotificationListCreateView(ListCreateAPIView):
    """
    List all notifications or create a new notification.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Retrieve list of all notifications",
        responses={200: NotificationSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                "channel",
                openapi.IN_QUERY,
                description="Filter notifications by channel",
                type=openapi.TYPE_STRING,
                enum=["email", "sms", "push", "in_app"],
            ),
            openapi.Parameter(
                "step_id",
                openapi.IN_QUERY,
                description="Filter notifications by workflow step ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "trigger_on_entry",
                openapi.IN_QUERY,
                description="Filter by trigger on entry setting",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter by channel
        channel_filter = request.query_params.get("channel")
        if channel_filter:
            queryset = queryset.filter(channel=channel_filter)

        # Filter by step_id
        step_id = request.query_params.get("step_id")
        if step_id:
            queryset = queryset.filter(step_id=step_id)

        # Filter by trigger_on_entry
        trigger_on_entry = request.query_params.get("trigger_on_entry")
        if trigger_on_entry is not None:
            trigger_on_entry = trigger_on_entry.lower() == "true"
            queryset = queryset.filter(trigger_on_entry=trigger_on_entry)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new notification",
        request_body=NotificationCreateSerializer,
        responses={201: NotificationSerializer, 400: "Bad Request - Invalid data"},
    )
    def post(self, request, *args, **kwargs):
        # Use NotificationCreateSerializer for validation
        serializer = NotificationCreateSerializer(data=request.data)
        if serializer.is_valid():
            notification = serializer.save()
            # Return full notification data using NotificationSerializer
            response_serializer = NotificationSerializer(notification)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a notification instance.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]
    lookup_field = "notification_id"

    @swagger_auto_schema(
        operation_description="Retrieve a specific notification",
        responses={200: NotificationSerializer, 404: "Notification not found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific notification",
        request_body=NotificationSerializer,
        responses={
            200: NotificationSerializer,
            400: "Bad Request - Invalid data",
            404: "Notification not found",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific notification",
        request_body=NotificationSerializer,
        responses={
            200: NotificationSerializer,
            400: "Bad Request - Invalid data",
            404: "Notification not found",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific notification",
        responses={
            204: "Notification deleted successfully",
            404: "Notification not found",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ===============================
# WORKFLOW VIEWS
# ===============================


class WorkflowListCreateView(ListCreateAPIView):
    """
    List all workflows or create a new workflow.
    """

    queryset = Workflow.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WorkflowCreateSerializer
        return WorkflowSerializer

    @swagger_auto_schema(
        operation_description="List all workflows with optional filtering",
        manual_parameters=[
            openapi.Parameter(
                "job_id",
                openapi.IN_QUERY,
                description="Filter workflows by job ID",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={200: WorkflowSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter by job_id
        job_id = request.query_params.get("job_id")
        if job_id:
            queryset = queryset.filter(job_id=job_id)

        serializer = WorkflowSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new workflow",
        request_body=WorkflowCreateSerializer,
        responses={201: WorkflowSerializer, 400: "Bad Request - Invalid data"},
    )
    def post(self, request, *args, **kwargs):
        serializer = WorkflowCreateSerializer(data=request.data)
        if serializer.is_valid():
            workflow = serializer.save()
            response_serializer = WorkflowSerializer(workflow)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkflowDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a workflow instance.
    """

    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = [AllowAny]
    lookup_field = "workflow_id"

    @swagger_auto_schema(
        operation_description="Retrieve a specific workflow",
        responses={200: WorkflowSerializer, 404: "Workflow not found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific workflow",
        request_body=WorkflowSerializer,
        responses={
            200: WorkflowSerializer,
            400: "Bad Request - Invalid data",
            404: "Workflow not found",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific workflow",
        request_body=WorkflowSerializer,
        responses={
            200: WorkflowSerializer,
            400: "Bad Request - Invalid data",
            404: "Workflow not found",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific workflow",
        responses={
            204: "Workflow deleted successfully",
            404: "Workflow not found",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ===============================
# WORKFLOW STEP VIEWS
# ===============================


class WorkflowStepListCreateView(ListCreateAPIView):
    """
    List all workflow steps or create a new workflow step.
    """

    queryset = WorkflowStep.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WorkflowStepCreateSerializer
        return WorkflowStepSerializer

    @swagger_auto_schema(
        operation_description="List all workflow steps with optional filtering",
        manual_parameters=[
            openapi.Parameter(
                "workflow_id",
                openapi.IN_QUERY,
                description="Filter steps by workflow ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "step_type",
                openapi.IN_QUERY,
                description="Filter steps by type",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "is_active",
                openapi.IN_QUERY,
                description="Filter by active status",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={200: WorkflowStepSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter by workflow_id
        workflow_id = request.query_params.get("workflow_id")
        if workflow_id:
            queryset = queryset.filter(workflow_id=workflow_id)

        # Filter by step_type
        step_type = request.query_params.get("step_type")
        if step_type:
            queryset = queryset.filter(step_type=step_type)

        # Filter by is_active
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)

        serializer = WorkflowStepSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new workflow step",
        request_body=WorkflowStepCreateSerializer,
        responses={201: WorkflowStepSerializer, 400: "Bad Request - Invalid data"},
    )
    def post(self, request, *args, **kwargs):
        serializer = WorkflowStepCreateSerializer(data=request.data)
        if serializer.is_valid():
            workflow_step = serializer.save()
            response_serializer = WorkflowStepSerializer(workflow_step)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkflowStepDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a workflow step instance.
    """

    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    permission_classes = [AllowAny]
    lookup_field = "step_id"

    @swagger_auto_schema(
        operation_description="Retrieve a specific workflow step",
        responses={200: WorkflowStepSerializer, 404: "Workflow step not found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific workflow step",
        request_body=WorkflowStepSerializer,
        responses={
            200: WorkflowStepSerializer,
            400: "Bad Request - Invalid data",
            404: "Workflow step not found",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific workflow step",
        request_body=WorkflowStepSerializer,
        responses={
            200: WorkflowStepSerializer,
            400: "Bad Request - Invalid data",
            404: "Workflow step not found",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific workflow step",
        responses={
            204: "Workflow step deleted successfully",
            404: "Workflow step not found",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ===============================
# WORKFLOW TEMPLATE VIEWS
# ===============================


class WorkflowTemplateListCreateView(ListCreateAPIView):
    """
    List all workflow templates or create a new workflow template.
    """

    queryset = WorkflowTemplate.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WorkflowTemplateCreateSerializer
        return WorkflowTemplateSerializer

    @swagger_auto_schema(
        operation_description="List all workflow templates with optional filtering",
        manual_parameters=[
            openapi.Parameter(
                "is_active",
                openapi.IN_QUERY,
                description="Filter by active status",
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                "name",
                openapi.IN_QUERY,
                description="Filter by template name (partial match)",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={200: WorkflowTemplateSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter by is_active
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)

        # Filter by name (partial match)
        name = request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        serializer = WorkflowTemplateSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new workflow template",
        request_body=WorkflowTemplateCreateSerializer,
        responses={201: WorkflowTemplateSerializer, 400: "Bad Request - Invalid data"},
    )
    def post(self, request, *args, **kwargs):
        serializer = WorkflowTemplateCreateSerializer(data=request.data)
        if serializer.is_valid():
            template = serializer.save()
            response_serializer = WorkflowTemplateSerializer(template)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkflowTemplateDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a workflow template instance.
    """

    queryset = WorkflowTemplate.objects.all()
    serializer_class = WorkflowTemplateSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    @swagger_auto_schema(
        operation_description="Retrieve a specific workflow template",
        responses={200: WorkflowTemplateSerializer, 404: "Workflow template not found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific workflow template",
        request_body=WorkflowTemplateSerializer,
        responses={
            200: WorkflowTemplateSerializer,
            400: "Bad Request - Invalid data",
            404: "Workflow template not found",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific workflow template",
        request_body=WorkflowTemplateSerializer,
        responses={
            200: WorkflowTemplateSerializer,
            400: "Bad Request - Invalid data",
            404: "Workflow template not found",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific workflow template",
        responses={
            204: "Workflow template deleted successfully",
            404: "Workflow template not found",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ===============================
# WORKFLOW STAGE TEMPLATE VIEWS
# ===============================


class WorkflowStageTemplateListCreateView(ListCreateAPIView):
    """
    List all workflow stage templates or create a new workflow stage template.
    """

    queryset = WorkflowStageTemplate.objects.all()
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return WorkflowStageTemplateCreateSerializer
        return WorkflowStageTemplateSerializer

    @swagger_auto_schema(
        operation_description="List all workflow stage templates with optional filtering",
        manual_parameters=[
            openapi.Parameter(
                "template_id",
                openapi.IN_QUERY,
                description="Filter stages by template ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                "stage_type",
                openapi.IN_QUERY,
                description="Filter stages by type",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "is_active",
                openapi.IN_QUERY,
                description="Filter by active status",
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
        responses={200: WorkflowStageTemplateSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Filter by template_id
        template_id = request.query_params.get("template_id")
        if template_id:
            queryset = queryset.filter(template_id=template_id)

        # Filter by stage_type
        stage_type = request.query_params.get("stage_type")
        if stage_type:
            queryset = queryset.filter(stage_type=stage_type)

        # Filter by is_active
        is_active = request.query_params.get("is_active")
        if is_active is not None:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(is_active=is_active)

        serializer = WorkflowStageTemplateSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new workflow stage template",
        request_body=WorkflowStageTemplateCreateSerializer,
        responses={
            201: WorkflowStageTemplateSerializer,
            400: "Bad Request - Invalid data",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = WorkflowStageTemplateCreateSerializer(data=request.data)
        if serializer.is_valid():
            stage_template = serializer.save()
            response_serializer = WorkflowStageTemplateSerializer(stage_template)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkflowStageTemplateDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a workflow stage template instance.
    """

    queryset = WorkflowStageTemplate.objects.all()
    serializer_class = WorkflowStageTemplateSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    @swagger_auto_schema(
        operation_description="Retrieve a specific workflow stage template",
        responses={
            200: WorkflowStageTemplateSerializer,
            404: "Workflow stage template not found",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific workflow stage template",
        request_body=WorkflowStageTemplateSerializer,
        responses={
            200: WorkflowStageTemplateSerializer,
            400: "Bad Request - Invalid data",
            404: "Workflow stage template not found",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific workflow stage template",
        request_body=WorkflowStageTemplateSerializer,
        responses={
            200: WorkflowStageTemplateSerializer,
            400: "Bad Request - Invalid data",
            404: "Workflow stage template not found",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific workflow stage template",
        responses={
            204: "Workflow stage template deleted successfully",
            404: "Workflow stage template not found",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# ===============================
# WORKFLOW FROM TEMPLATE VIEW
# ===============================


class WorkflowFromTemplateView(APIView):
    """
    Create a workflow from a template.
    """

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Create a workflow from a template",
        request_body=WorkflowFromTemplateSerializer,
        responses={
            201: WorkflowSerializer,
            400: "Bad Request - Invalid data",
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = WorkflowFromTemplateSerializer(data=request.data)
        if serializer.is_valid():
            workflow = serializer.save()
            response_serializer = WorkflowSerializer(workflow)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
