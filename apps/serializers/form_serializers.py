from rest_framework import serializers
from apps.models.form_models import Form, Question, Option, UserAnswer


class FormSerializer(serializers.ModelSerializer):

    class Meta:
        model = Form
        exclude = ['trashed', 'trashed_at']


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        exclude = ['trashed', 'trashed_at']


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        exclude = ['trashed', 'trashed_at']


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        exclude = ['trashed', 'trashed_at']
