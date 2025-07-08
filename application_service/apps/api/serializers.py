from rest_framework import serializers
from .models.job import JobDescription
from .models.application import Application

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
