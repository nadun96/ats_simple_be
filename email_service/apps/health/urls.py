from django.urls import path
from .views import health_check, health_detailed

urlpatterns = [
    path("", health_check, name="health_check"),
    path("detailed/", health_detailed, name="health_detailed"),
]
