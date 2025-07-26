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
]
