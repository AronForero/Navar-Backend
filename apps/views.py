from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from apps.models import Requirement, Service, Request
from authentication.models import User
from apps.serializers import RequirementSerializer, ServiceSerializer, RequestSerializer


class RequirementViewSet(viewsets.ModelViewSet):
    queryset = Requirement.objects.filter(trashed=False)
    serializer_class = RequirementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        req_obj = get_object_or_404(Requirement, id=kwargs.get('pk'))
        req_obj.trashed = True
        req_obj.trashed_at = datetime.now()
        req_obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(trashed=False)
    serializer_class = ServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        service_obj = get_object_or_404(Service, id=kwargs.get('pk'))
        service_obj.trashed = True
        service_obj.trashed_at = datetime.now()
        service_obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.filter(trashed=False)
    serializer_class = RequestSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        """ This function is for the super user """
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        request_obj = get_object_or_404(Request, id=kwargs.get('pk'))

        request_obj_2 = Request.objects.create(**self.serializer_class(request_obj).data)
        Request.objects.update(id=request_obj_2.id, **serializer.validated_data)
        request_obj_2 = Request.objects.get(id=request_obj_2.id)
        
        request_obj.trashed = True
        request_obj.trashed_at = datetime.now()
        request_obj.save()
        return Response(self.serializer_class(request_obj_2).data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        current_user = User.objects.get(id=self.request.user.id)
        if not current_user.is_superuser:
            return Response('Only Super User allowed', status=status.HTTP_400_BAD_REQUEST)
        request_obj = get_object_or_404(Request, id=kwargs.get('pk'))
        request_obj.trashed = True
        request_obj.trashed_at = datetime.now()
        request_obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorizeRequest(viewsets.generics.UpdateAPIView):

    def update(self, request, *args, **kwargs):
        """ This Function is for the specialist person """
        serializer = RequestSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        request_obj = get_object_or_404(Request, id=kwargs.get('pk'))
        request_obj.inspected_by = serializer.validated_data.get('inspected_by')
        request_obj.inspected_at = datetime.now()
        request_obj.save()

        return Response(self.serializer_class(request_obj).data, status=status.HTTP_200_OK)

