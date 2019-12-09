from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class PublicUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(
            validated_data.pop("email"),
            password=validated_data.pop("password"),
            **validated_data,
        )

    def update(self, instance, validated_data):
        if validated_data.get('password', None):
            instance.set_password(validated_data.pop("password"))
        super(self.__class__, self).update(instance, validated_data)
        return instance

    class Meta:
        model = User
        # we don't want to return password
        exclude = [
            'trashed',
            'trashed_at',
            'user_type',
        ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            'password',
            'thrashed',
            'thrashed_at',
        ]
