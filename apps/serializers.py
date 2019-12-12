from rest_framework import serializers
from apps.models import Requirement, Service, Request, RequestComment, RequestService, Case, CaseRequirement


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


class RequestCommentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=500)


class CommentsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    content = serializers.CharField(max_length=500),
    request__tag = serializers.CharField(max_length=15)
    created_by__email = serializers.EmailField()


class RequestServiceSerializer(serializers.Serializer):
    price = serializers.FloatField()
    quantity = serializers.IntegerField()


class RequestServiceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestService
        exclude = ['trashed', 'trashed_at', 'updated_at']


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        exclude = ['trashed', 'trashed_at']


class CaseRequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseRequirement
        exclude = ['trashed', 'trashed_at', 'updated_at']
