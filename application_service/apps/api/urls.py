from django.urls import path 
from .views import (
    # Main Job endpoints
    JobListCreateView,
    JobDetailView,
    CompleteJobCreateView,
    # Society endpoints
    SocietyListCreateView,
    SocietyDetailView,
    # JobForm endpoints
    JobFormListCreateView,
    JobFormDetailView,
    # FormField endpoints
    FormFieldListCreateView,
    FormFieldDetailView,
    # Team endpoints
    TeamListCreateView,
    TeamDetailView,
    # TeamMember endpoints
    TeamMemberListCreateView,
    TeamMemberDetailView,
    # WorkflowTemplate endpoints
    WorkflowTemplateListCreateView,
    WorkflowTemplateDetailView,
    # WorkflowStep endpoints
    WorkflowStepListCreateView,
    WorkflowStepDetailView,
    # WorkflowAction endpoints
    WorkflowActionListCreateView,
    WorkflowActionDetailView,
    # WorkflowTask endpoints
    WorkflowTaskListCreateView,
    WorkflowTaskDetailView,
    # TaskComment endpoints
    TaskCommentListCreateView,
    TaskCommentDetailView,
    # StepLink endpoints
    StepLinkListCreateView,
    StepLinkDetailView,
    # JobSite endpoints
    JobSiteListCreateView,
    JobSiteDetailView,
    # Legacy endpoints
    JobDescriptionView,
    ApplicationListView,
    JobDescriptionListView,
    # New Application and Candidate endpoints
    CandidateListCreateView,
    CandidateDetailView,
    ApplicationListCreateView,
    ApplicationDetailView,
    ApplicationAdvanceStageView,
    ApplicationMoveStageView,
)

urlpatterns = [
    # Main Job endpoints
    path("jobs/", JobListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:id>/", JobDetailView.as_view(), name="job-detail"),
    path("jobs/complete/", CompleteJobCreateView.as_view(), name="complete-job-create"),
    # Society endpoints
    path("societies/", SocietyListCreateView.as_view(), name="society-list-create"),
    path("societies/<int:id>/", SocietyDetailView.as_view(), name="society-detail"),
    # JobForm endpoints
    path("job-forms/", JobFormListCreateView.as_view(), name="job-form-list-create"),
    path("job-forms/<int:id>/", JobFormDetailView.as_view(), name="job-form-detail"),
    # FormField endpoints
    path(
        "form-fields/", FormFieldListCreateView.as_view(), name="form-field-list-create"
    ),
    path(
        "form-fields/<int:id>/", FormFieldDetailView.as_view(), name="form-field-detail"
    ),
    # Team endpoints
    path("teams/", TeamListCreateView.as_view(), name="team-list-create"),
    path("teams/<int:id>/", TeamDetailView.as_view(), name="team-detail"),
    # TeamMember endpoints
    path(
        "team-members/",
        TeamMemberListCreateView.as_view(),
        name="team-member-list-create",
    ),
    path(
        "team-members/<int:id>/",
        TeamMemberDetailView.as_view(),
        name="team-member-detail",
    ),
    # WorkflowTemplate endpoints
    path(
        "workflow-templates/",
        WorkflowTemplateListCreateView.as_view(),
        name="workflow-template-list-create",
    ),
    path(
        "workflow-templates/<int:id>/",
        WorkflowTemplateDetailView.as_view(),
        name="workflow-template-detail",
    ),
    # WorkflowStep endpoints
    path(
        "workflow-steps/",
        WorkflowStepListCreateView.as_view(),
        name="workflow-step-list-create",
    ),
    path(
        "workflow-steps/<int:id>/",
        WorkflowStepDetailView.as_view(),
        name="workflow-step-detail",
    ),
    # WorkflowAction endpoints
    path(
        "workflow-actions/",
        WorkflowActionListCreateView.as_view(),
        name="workflow-action-list-create",
    ),
    path(
        "workflow-actions/<int:id>/",
        WorkflowActionDetailView.as_view(),
        name="workflow-action-detail",
    ),
    # WorkflowTask endpoints
    path(
        "workflow-tasks/",
        WorkflowTaskListCreateView.as_view(),
        name="workflow-task-list-create",
    ),
    path(
        "workflow-tasks/<int:id>/",
        WorkflowTaskDetailView.as_view(),
        name="workflow-task-detail",
    ),
    # TaskComment endpoints
    path(
        "task-comments/",
        TaskCommentListCreateView.as_view(),
        name="task-comment-list-create",
    ),
    path(
        "task-comments/<int:id>/",
        TaskCommentDetailView.as_view(),
        name="task-comment-detail",
    ),
    # StepLink endpoints
    path("step-links/", StepLinkListCreateView.as_view(), name="step-link-list-create"),
    path("step-links/<int:id>/", StepLinkDetailView.as_view(), name="step-link-detail"),
    # JobSite endpoints
    path("job-sites/", JobSiteListCreateView.as_view(), name="job-site-list-create"),
    path("job-sites/<int:id>/", JobSiteDetailView.as_view(), name="job-site-detail"),
    # Legacy endpoints
    path("job-description/", JobDescriptionView.as_view(), name="job-description"),
    path(
        "job-descriptions/",
        JobDescriptionListView.as_view(),
        name="job-description-list",
    ),
    path("applications/", ApplicationListView.as_view(), name="application-list"),
    # ===== NEW APPLICATION & CANDIDATE ENDPOINTS =====
    # Candidate endpoints
    path(
        "candidates/", CandidateListCreateView.as_view(), name="candidate-list-create"
    ),
    path(
        "candidates/<int:candidate_id>/",
        CandidateDetailView.as_view(),
        name="candidate-detail",
    ),
    # Enhanced Application endpoints
    path(
        "v2/applications/",
        ApplicationListCreateView.as_view(),
        name="application-v2-list-create",
    ),
    path(
        "v2/applications/<int:application_id>/",
        ApplicationDetailView.as_view(),
        name="application-v2-detail",
    ),
    path(
        "v2/applications/<int:application_id>/advance/",
        ApplicationAdvanceStageView.as_view(),
        name="application-advance-stage",
    ),
    path(
        "v2/applications/<int:application_id>/move-stage/",
        ApplicationMoveStageView.as_view(),
        name="application-move-stage",
    ),
]
