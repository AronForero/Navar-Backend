from rest_framework import serializers
from apps.models import Requirement, Service, Request


class RequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requirement
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']
