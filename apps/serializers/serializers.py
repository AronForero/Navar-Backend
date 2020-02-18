from rest_framework import serializers
from apps.models.models import Request, UserRequest, RequestService, ActivityRequest, ActivityRequestComment, \
 ActivityRequestPrevious, RequestFileOutput, RequestFileInput, File, Quotation, Requirement, Case, CaseRequirement


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class UserRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRequest
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class RequestServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestService
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class ActivityRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityRequest
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class ActivityRequestCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityRequestComment
        exclude = ['created_at', 'updated_at']


class ActivityRequestPrevious(serializers.ModelSerializer):

    class Meta:
        model = ActivityRequestPrevious
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class RequestFileOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestFileOutput
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class RequestFileInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequestFileInput
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        exclude = ['created_at', 'updated_at']


class QuotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quotation
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class RequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Requirement
        exclude = ['created_at', 'updated_at', 'trashed', 'trashed_at']


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        exclude = ['trashed', 'trashed_at']


class CaseRequirementSerializer(serializers.ModelSerializer):

    class Meta:
        model = CaseRequirement
        exclude = ['trashed', 'trashed_at', 'updated_at']
