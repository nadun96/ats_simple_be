from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmailTemplateViewSet,
    EmailViewSet,
    ScheduledTaskViewSet,
    EmailQueueViewSet,
)

router = DefaultRouter()
router.register(r"templates", EmailTemplateViewSet)
router.register(r"emails", EmailViewSet)
router.register(r"scheduled-tasks", ScheduledTaskViewSet)
router.register(r"queue", EmailQueueViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
