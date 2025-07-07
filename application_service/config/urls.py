from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', include('apps.health.urls')),
    path('api/v1/', include('apps.api.urls')),
]
