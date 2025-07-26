from django.urls import path 
from .views import (
    JobDescriptionView,
    ApplicationListView,
    JobDescriptionListView,
    TaskListCreateView,
    TaskDetailView,
    NotificationListCreateView,
    NotificationDetailView,
    WorkflowListCreateView,
    WorkflowDetailView,
    WorkflowStepListCreateView,
    WorkflowStepDetailView,
    WorkflowTemplateListCreateView,
    WorkflowTemplateDetailView,
    WorkflowStageTemplateListCreateView,
    WorkflowStageTemplateDetailView,
    WorkflowFromTemplateView,
)

urlpatterns = [
    # Existing endpoints
    path("job-description/", JobDescriptionView.as_view(), name="job-description"),
    path(
        "job-descriptions/",
        JobDescriptionListView.as_view(),
        name="job-description-list",
    ),
    path("applications/", ApplicationListView.as_view(), name="application-list"),
    # Task endpoints
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:task_id>/", TaskDetailView.as_view(), name="task-detail"),
    # Notification endpoints
    path(
        "notifications/",
        NotificationListCreateView.as_view(),
        name="notification-list-create",
    ),
    path(
        "notifications/<int:notification_id>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    # Workflow endpoints
    path(
        "workflows/",
        WorkflowListCreateView.as_view(),
        name="workflow-list-create",
    ),
    path(
        "workflows/<int:workflow_id>/",
        WorkflowDetailView.as_view(),
        name="workflow-detail",
    ),
    # Workflow Step endpoints
    path(
        "workflow-steps/",
        WorkflowStepListCreateView.as_view(),
        name="workflow-step-list-create",
    ),
    path(
        "workflow-steps/<int:step_id>/",
        WorkflowStepDetailView.as_view(),
        name="workflow-step-detail",
    ),
    # Workflow Template endpoints
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
    # Workflow Stage Template endpoints
    path(
        "workflow-stage-templates/",
        WorkflowStageTemplateListCreateView.as_view(),
        name="workflow-stage-template-list-create",
    ),
    path(
        "workflow-stage-templates/<int:id>/",
        WorkflowStageTemplateDetailView.as_view(),
        name="workflow-stage-template-detail",
    ),
    # Workflow from Template endpoint
    path(
        "workflows/create-from-template/",
        WorkflowFromTemplateView.as_view(),
        name="workflow-create-from-template",
    ),
]
