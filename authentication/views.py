from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from authentication.models import User, AdditionalUserInformation, Role, UserRole
from authentication.serializers import PublicUserSerializer, AdditionalUserInfoSerializer, PublicUpdateSerializer,\
 RoleSerializer, UserRoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        user_serializer = PublicUserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)

        user = User.objects.create_user(**user_serializer.validated_data)
        # user = User.objects.create_superuser(**user_serializer.validated_data)
        user.save()

        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(trashed=False)
        return Response(self.serializer_class(users, many=True).data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        serializer = PublicUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Validate fields
        password = serializer.validated_data.get('password')
        if password is not None:
            current_user.set_password(password)

        if serializer.validated_data.get('first_name') is not None:
            current_user.first_name = serializer.validated_data.get('first_name')
        if serializer.validated_data.get('last_name') is not None:
            current_user.last_name = serializer.validated_data.get('last_name')

        current_user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDeleteView(viewsets.generics.DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=kwargs.get('user_id'))
        user.trashed = True
        user.trashed_at = datetime.now()
        user.save()
        extra_info = AdditionalUserInformation.objects.get(user=user, trashed=False)
        extra_info.trashed = True
        extra_info.trashed_at = datetime.now()
        extra_info.save()
        return Response({'detail': 'deleted.'}, status=status.HTTP_200_OK)


class AdditionalUserDataViewSet(viewsets.ModelViewSet):
    queryset = AdditionalUserInformation.objects.all()
    serializer_class = AdditionalUserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        """
        This function reach an object and returns it
        """
        user = User.objects.get(id=self.request.user.id)
        user_info = get_object_or_404(AdditionalUserInformation, user=user, trashed=False)

        return Response(self.serializer_class(user_info).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        This function allow us to create the extra user info object
        """
        request.data['user'] = self.request.user.id
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
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
        This function allow to update a specific user info in the DB
        """
        user = User.objects.get(id=self.request.user.id, trashed=False)
        request.data['user'] = self.request.user.id
        extra_info = AdditionalUserInformation.objects.filter(user=user, trashed=False)
        if len(extra_info) > 1:
            return Response({'detail': 'more than one object found, please contact the administrator of the system'},
                            status=status.HTTP_409_CONFLICT)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        AdditionalUserInformation.objects.update(**serializer.validated_data)
        user_info = AdditionalUserInformation.objects.get(user=user)

        return Response(self.serializer_class(user_info).data, status=status.HTTP_200_OK)


class RolesViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.filter(trashed=False)
    serializer_class = UserRoleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        role = get_object_or_404(Role, id=kwargs.get('role_id'))

        user_role = UserRole.objects.create(user=user, role=role)

        return Response(self.serializer_class(user_role).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=kwargs.get('user_id'))
        role = get_object_or_404(Role, id=kwargs.get('role_id'))
        
        user_role = get_object_or_404(UserRole, user=user, role=role, trashed=False)
        user_role.trashed = True
        user_role.trashed_at = datetime.now()
        user_role.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
