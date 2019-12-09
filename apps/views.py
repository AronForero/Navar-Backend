from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from apps.models.user import User
from apps.serializers.user_serializers import PublicUserSerializer, UserSerializer


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



