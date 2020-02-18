from rest_framework import serializers
from apps.models.abstract_models import Service, Activity, ActivityOrder, FileInput, FileOutput


class AbstractServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class AbstractActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Activity
        fields = '__all__'


class AbstractActivityOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityOrder
        fields = '__all__'


class AbstractFileInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileInput
        fields = '__all__'


class AbstractFileOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileOutput
        fields = '__all__'
