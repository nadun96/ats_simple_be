from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import (
    JobDescriptionSerializer,
    ApplicationSerializer,
    JobSerializer,
    CompleteJobSerializer,
    SocietySerializer,
    JobFormSerializer,
    FormFieldSerializer,
    TeamSerializer,
    TeamMemberSerializer,
    WorkflowTemplateSerializer,
    WorkflowStepSerializer,
    WorkflowActionSerializer,
    WorkflowTaskSerializer,
    TaskCommentSerializer,
    StepLinkSerializer,
    JobSiteSerializer,
    # New serializers
    CandidateSerializer,
    DetailedApplicationSerializer,
    CreateApplicationSerializer,
    ApplicationUpdateSerializer,
    ApplicationStageHistorySerializer,
    ApplicationFormAnswerSerializer,
)
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
from .models.application import (
    Application,
    ApplicationStageHistory,
    ApplicationFormAnswer,
)
from .models.candidate import Candidate


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# ===== JOB MAIN ENDPOINTS =====


class JobListCreateView(ListCreateAPIView):
    """List all jobs with pagination or create a new job"""

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Get all jobs with pagination",
        responses={200: JobSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new job",
        request_body=JobSerializer,
        responses={201: JobSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class JobDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific job"""

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    @swagger_auto_schema(
        operation_description="Get job by ID",
        responses={200: JobSerializer, 404: "Job not found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update job by ID",
        request_body=JobSerializer,
        responses={200: JobSerializer, 404: "Job not found"},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete job by ID",
        responses={204: "Job deleted successfully", 404: "Job not found"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CompleteJobCreateView(APIView):
    """Create a complete job with all nested data from frontend JSON structure"""

    permission_classes = [AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Create a complete job with all metadata at once",
        request_body=CompleteJobSerializer,
        responses={201: JobSerializer, 400: "Validation errors"},
    )
    def post(self, request):
        # Extract the job data from the nested structure
        job_data = request.data.get("job", {})
        description_data = job_data.get("description", {})

        # Flatten the nested structure for the serializer
        flattened_data = {}

        # Extract job description fields
        job_desc = description_data.get("job description", {})
        flattened_data.update(job_desc)

        # Extract other nested data
        flattened_data["society"] = description_data.get("society")
        flattened_data["settings"] = description_data.get("settings")
        flattened_data["tag"] = description_data.get("tag")
        flattened_data["JobForm"] = job_data.get("JobForm")
        flattened_data["Team"] = job_data.get("Team")
        flattened_data["WorkFlow"] = job_data.get("WorkFlow")
        flattened_data["sites"] = job_data.get("sites")

        serializer = CompleteJobSerializer(data=flattened_data)
        if serializer.is_valid():
            job = serializer.save()
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ===== SOCIETY ENDPOINTS =====


class SocietyListCreateView(ListCreateAPIView):
    """List all societies or create a new society"""

    queryset = Society.objects.all()
    serializer_class = SocietySerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class SocietyDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific society"""

    queryset = Society.objects.all()
    serializer_class = SocietySerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== JOB FORM ENDPOINTS =====


class JobFormListCreateView(ListCreateAPIView):
    """List all job forms or create a new job form"""

    queryset = JobForm.objects.all()
    serializer_class = JobFormSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class JobFormDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific job form"""

    queryset = JobForm.objects.all()
    serializer_class = JobFormSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== FORM FIELD ENDPOINTS =====


class FormFieldListCreateView(ListCreateAPIView):
    """List all form fields or create a new form field"""

    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class FormFieldDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific form field"""

    queryset = FormField.objects.all()
    serializer_class = FormFieldSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== TEAM ENDPOINTS =====


class TeamListCreateView(ListCreateAPIView):
    """List all teams or create a new team"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class TeamDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific team"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== TEAM MEMBER ENDPOINTS =====


class TeamMemberListCreateView(ListCreateAPIView):
    """List all team members or create a new team member"""

    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class TeamMemberDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific team member"""

    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== WORKFLOW TEMPLATE ENDPOINTS =====


class WorkflowTemplateListCreateView(ListCreateAPIView):
    """List all workflow templates or create a new workflow template"""

    queryset = WorkflowTemplate.objects.all()
    serializer_class = WorkflowTemplateSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class WorkflowTemplateDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific workflow template"""

    queryset = WorkflowTemplate.objects.all()
    serializer_class = WorkflowTemplateSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== WORKFLOW STEP ENDPOINTS =====


class WorkflowStepListCreateView(ListCreateAPIView):
    """List all workflow steps or create a new workflow step"""

    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class WorkflowStepDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific workflow step"""

    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== WORKFLOW ACTION ENDPOINTS =====


class WorkflowActionListCreateView(ListCreateAPIView):
    """List all workflow actions or create a new workflow action"""

    queryset = WorkflowAction.objects.all()
    serializer_class = WorkflowActionSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class WorkflowActionDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific workflow action"""

    queryset = WorkflowAction.objects.all()
    serializer_class = WorkflowActionSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== WORKFLOW TASK ENDPOINTS =====


class WorkflowTaskListCreateView(ListCreateAPIView):
    """List all workflow tasks or create a new workflow task"""

    queryset = WorkflowTask.objects.all()
    serializer_class = WorkflowTaskSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class WorkflowTaskDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific workflow task"""

    queryset = WorkflowTask.objects.all()
    serializer_class = WorkflowTaskSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== TASK COMMENT ENDPOINTS =====


class TaskCommentListCreateView(ListCreateAPIView):
    """List all task comments or create a new task comment"""

    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class TaskCommentDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific task comment"""

    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== STEP LINK ENDPOINTS =====


class StepLinkListCreateView(ListCreateAPIView):
    """List all step links or create a new step link"""

    queryset = StepLink.objects.all()
    serializer_class = StepLinkSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class StepLinkDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific step link"""

    queryset = StepLink.objects.all()
    serializer_class = StepLinkSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== JOB SITE ENDPOINTS =====


class JobSiteListCreateView(ListCreateAPIView):
    """List all job sites or create a new job site"""

    queryset = JobSite.objects.all()
    serializer_class = JobSiteSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class JobSiteDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific job site"""

    queryset = JobSite.objects.all()
    serializer_class = JobSiteSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"


# ===== LEGACY ENDPOINTS =====


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
            return Response(
                JobDescriptionSerializer(job_desc).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationListView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


class JobDescriptionListView(ListAPIView):
    queryset = JobDescription.objects.all()
    serializer_class = JobDescriptionSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination


# ===== ENHANCED APPLICATION & CANDIDATE ENDPOINTS =====


class CandidateListCreateView(ListCreateAPIView):
    """List all candidates or create a new candidate"""

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Get all candidates with pagination",
        responses={200: CandidateSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new candidate",
        request_body=CandidateSerializer,
        responses={201: CandidateSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CandidateDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific candidate"""

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]
    lookup_field = "candidate_id"
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Get candidate by ID",
        responses={200: CandidateSerializer, 404: "Candidate not found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update candidate by ID",
        request_body=CandidateSerializer,
        responses={200: CandidateSerializer, 404: "Candidate not found"},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete candidate by ID",
        responses={204: "Candidate deleted successfully", 404: "Candidate not found"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ApplicationListCreateView(ListCreateAPIView):
    """List all applications or create a new application with candidate and job form data"""

    queryset = Application.objects.all()
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateApplicationSerializer
        return DetailedApplicationSerializer

    @swagger_auto_schema(
        operation_description="Get all applications with detailed information",
        responses={200: DetailedApplicationSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new application with candidate and form data",
        request_body=CreateApplicationSerializer,
        responses={201: DetailedApplicationSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save()

            # Trigger workflow actions for the initial stage
            self._trigger_stage_actions(application, application.current_stage)

            response_serializer = DetailedApplicationSerializer(application)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _trigger_stage_actions(self, application, stage):
        """Trigger actions (emails, notifications, tasks) for a workflow stage"""
        if not stage:
            return

        # Process workflow actions
        for action in stage.actions.all():
            if action.action_type == "email":
                self._send_email_notification(application, action)
            elif action.action_type == "notification":
                self._send_notification(application, action)
            elif action.action_type == "task":
                self._create_task(application, action)

    def _send_email_notification(self, application, action):
        """Send email notification (would integrate with email service)"""
        # This would integrate with your email service
        # For now, just logging the action
        print(f"Email notification triggered for {application} - {action.action_name}")

    def _send_notification(self, application, action):
        """Send in-app notification"""
        # This would integrate with your notification service
        print(f"Notification triggered for {application} - {action.action_name}")

    def _create_task(self, application, action):
        """Create workflow task"""
        # This would create tasks for team members
        print(f"Task created for {application} - {action.action_name}")


class ApplicationDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a specific application"""

    queryset = Application.objects.all()
    permission_classes = [AllowAny]
    lookup_field = "application_id"
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ApplicationUpdateSerializer
        return DetailedApplicationSerializer

    @swagger_auto_schema(
        operation_description="Get application by ID with full details",
        responses={200: DetailedApplicationSerializer, 404: "Application not found"},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update application by ID",
        request_body=ApplicationUpdateSerializer,
        responses={200: DetailedApplicationSerializer, 404: "Application not found"},
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete application by ID",
        responses={
            204: "Application deleted successfully",
            404: "Application not found",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class ApplicationAdvanceStageView(APIView):
    """Advance application to next workflow stage"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Move application to next workflow stage",
        responses={
            200: "Application advanced successfully",
            404: "Application not found",
            400: "Cannot advance further",
        },
    )
    def post(self, request, application_id):
        try:
            application = Application.objects.get(application_id=application_id)

            if application.advance_to_next_stage():
                # Create stage history
                ApplicationStageHistory.objects.create(
                    application=application,
                    from_stage=application.current_stage,
                    to_stage=application.current_stage,
                    changed_by=request.user.username
                    if hasattr(request.user, "username")
                    else "system",
                    notes="Advanced to next stage",
                )

                # Trigger stage actions
                self._trigger_stage_actions(application, application.current_stage)

                serializer = DetailedApplicationSerializer(application)
                return Response(
                    {
                        "message": "Application advanced successfully",
                        "application": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Cannot advance application further"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Application.DoesNotExist:
            return Response(
                {"message": "Application not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def _trigger_stage_actions(self, application, stage):
        """Trigger actions for the new stage"""
        if not stage:
            return

        for action in stage.actions.all():
            if action.action_type == "email":
                self._send_email_notification(application, action)
            elif action.action_type == "notification":
                self._send_notification(application, action)
            elif action.action_type == "task":
                self._create_task(application, action)

    def _send_email_notification(self, application, action):
        print(f"Email notification triggered for {application} - {action.action_name}")

    def _send_notification(self, application, action):
        print(f"Notification triggered for {application} - {action.action_name}")

    def _create_task(self, application, action):
        print(f"Task created for {application} - {action.action_name}")


class ApplicationMoveStageView(APIView):
    """Move application to specific workflow stage"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Move application to specific workflow stage",
        request_body=None,  # Define a proper serializer for this
        responses={
            200: "Application moved successfully",
            404: "Application not found",
            400: "Invalid stage",
        },
    )
    def post(self, request, application_id):
        stage_id = request.data.get("stage_id")
        notes = request.data.get("notes", "")

        if not stage_id:
            return Response(
                {"message": "stage_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            application = Application.objects.get(application_id=application_id)
            old_stage = application.current_stage

            if application.move_to_stage(stage_id):
                # Create stage history
                ApplicationStageHistory.objects.create(
                    application=application,
                    from_stage=old_stage,
                    to_stage=application.current_stage,
                    changed_by=request.user.username
                    if hasattr(request.user, "username")
                    else "system",
                    notes=notes,
                )

                # Trigger stage actions
                self._trigger_stage_actions(application, application.current_stage)

                serializer = DetailedApplicationSerializer(application)
                return Response(
                    {
                        "message": "Application moved successfully",
                        "application": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"message": "Invalid stage for this job"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Application.DoesNotExist:
            return Response(
                {"message": "Application not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def _trigger_stage_actions(self, application, stage):
        """Trigger actions for the new stage"""
        if not stage:
            return

        for action in stage.actions.all():
            if action.action_type == "email":
                self._send_email_notification(application, action)
            elif action.action_type == "notification":
                self._send_notification(application, action)
            elif action.action_type == "task":
                self._create_task(application, action)

    def _send_email_notification(self, application, action):
        print(f"Email notification triggered for {application} - {action.action_name}")

    def _send_notification(self, application, action):
        print(f"Notification triggered for {application} - {action.action_name}")

    def _create_task(self, application, action):
        print(f"Task created for {application} - {action.action_name}")
