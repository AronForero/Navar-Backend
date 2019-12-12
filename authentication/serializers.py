from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from authentication.models import Role, UserRole, User, AdditionalUserInformation


class PublicUserSerializer(UserCreateSerializer):

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

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['email', 'id', 'password', 'first_name', 'last_name']


class PublicUpdateSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, allow_null=True)
    first_name = serializers.CharField(max_length=20, allow_null=True)
    last_name = serializers.CharField(max_length=30, allow_null=True)


class CustomUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']


class AdditionalUserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalUserInformation
        exclude = ('trashed', 'trashed_at', 'created_at', 'updated_at')


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role']
