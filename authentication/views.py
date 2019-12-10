from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from authentication.models import User, Role, UserRole, AdditionalUserInformation
from authentication.serializers import PublicUserSerializer, UserSerializer, RoleSerializer, UserRoleSerializer, \
    AdditionalUserInfoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        user_serializer = PublicUserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**user_serializer.validated_data)
        user.save()

        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(trashed=False)
        return Response(self.serializer_class(users, many=True).data, status=status.HTTP_200_OK)


class AdditionalUserDataViewSet(viewsets.ModelViewSet):
    queryset = AdditionalUserInformation.objects.all()
    serializer_class = AdditionalUserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=self.request.user.id)
        additional_info = AdditionalUserInformation.objects.filter(user=user)
        s = dict(list(additional_info.values())[0])
        print(self.serializer_class(s).data)
        serializer = self.serializer_class(s)
        serializer.is_valid(raise_exception=True)
        if len(additional_info) == 0:
            return Response({'detail': 'No Additional Info'})
        self.check_object_permissions(self.request, additional_info)

        return Response(self.serializer_class(additional_info, partial=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(id=request.data.get('user'))
        additional_info = AdditionalUserInformation.objects.filter(user=serializer.validated_data.get('user'))
        if len(additional_info) > 0:
            return Response({'detail': 'Additional Information object already exist, please do a PUT request instead.'})
        additional_info = AdditionalUserInformation.objects.create(
            **serializer.validated_data
        )
        additional_info.save()
        return Response(self.serializer_class(additional_info).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        This function allow to update a specific user in the DB
        """
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {
            self.lookup_field: self.request.user.id,
            'trashed': False,
            'is_active': True,
        }

        user = get_object_or_404(queryset, **filter_kwargs)

        user_serializer = PublicUserSerializer(user, data=request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(self.serializer_class(user).data, status=status.HTTP_200_OK)
