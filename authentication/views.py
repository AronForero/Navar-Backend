from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from authentication.models.user import User, Role, UserRole, AdditionalUserInformation
from authentication.serializers.user_serializers import PublicUserSerializer, UserSerializer, RoleSerializer, UserRoleSerializer


class CreateUserViewSet(viewsets.ModelViewSet):
    """
    View to create new users
    """
    queryset = User.objects.all()
    serializer_class = PublicUserSerializer
    permission_classes = (permissions.AllowAny,)
    parser_classes = (JSONParser,)

    def create(self, request, *args, **kwargs):
        """
        Function used to create a new user
        """
        user_serializer = self.serializer_class(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {
            self.lookup_field: self.request.user.id,
            'trashed': False,
            'is_active': True,
        }

        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)

        return Response(self.serializer_class(obj).data, status=status.HTTP_200_OK)

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


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        role_serializer = self.serializer_class(data=request.data)
        role_serializer.is_valid(raise_exception=True)
        roles = Role.objects.filter(name=request.data.get('name'), tag=request.data.get('tag'))
        if len(roles) != 0:
            return Response({'detail': 'Role already Exist!!'}, status=status.HTTP_409_CONFLICT)
        
        role = Role.objects.create(tag=request.data.get('tag'),
                                   name=request.data.get('name'),
                                   description=request.data.get('description'),
                                )
        role.save()
        return Response(self.serializer_class(role).data, status=status.HTTP_201_CREATED)


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(id=request.data.get('user'))
        role = get_object_or_404(id=request.data.get('role'))

        user_role = UserRole.objects.get(user=user, role=role)
        if user_role is not None:
            return Response({'detail': 'The user has already got this role.'}, status=status.HTTP_409_CONFLICT)
        user_role = UserRole.objects.create(user=user, role=role)
        user_role.save()
        
        return Response(self.serializer_class(user_role).data, status=status.HTTP_201_CREATED)
