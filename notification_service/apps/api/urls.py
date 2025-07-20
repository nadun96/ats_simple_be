from django.urls import path 
from .views import JobDescriptionView, ApplicationListView, JobDescriptionListView

urlpatterns = [
    path('job-description/', JobDescriptionView.as_view(), name='job-description'),
    path('job-descriptions/', JobDescriptionListView.as_view(), name='job-description-list'),
    path('applications/', ApplicationListView.as_view(), name='application-list'),
]
