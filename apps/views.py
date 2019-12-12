from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from apps.models import Requirement, Service, Request, RequestComment, RequestService, Case, CaseRequirement
from authentication.models import User
from apps.serializers import RequirementSerializer, ServiceSerializer, RequestSerializer, RequestCommentSerializer, \
    CommentsSerializer, RequestServiceSerializer, RequestServiceModelSerializer, CaseSerializer, \
    CaseRequirementSerializer


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
    # queryset = Request.objects.all()
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

        request_obj_2 = Request.objects.create(**serializer.validated_data)
        
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


class RequestCommentViewSet(viewsets.ModelViewSet):
    queryset = RequestComment.objects.all()
    serializer_class = RequestCommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        current_request = Request.objects.get(id=kwargs.get('pk'))
        comments = RequestComment.objects.filter(request=current_request).values('id', 'request__tag', 'created_by__email',
                                                                                 'content', 'created_at')
        serializer = CommentsSerializer(data=list(comments), many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_request = Request.objects.get(id=kwargs.get('pk'))
        current_user = User.objects.get(id=self.request.user.id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_comment = RequestComment.objects.create(request=current_request, created_by=current_user,
                                                    **serializer.validated_data)

        new_comment = new_comment.__dict__
        del new_comment['_state']
        del new_comment['updated_at']
        return Response(new_comment, status=status.HTTP_201_CREATED)


class RequestServiceViewSet(viewsets.ModelViewSet):
    queryset = RequestService.objects.all()
    serializer_class = RequestServiceSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        current_request = Request.objects.get(id=kwargs.get('request_id'))
        request_services = RequestService.objects.filter(request=current_request, trashed=False)
        return Response(RequestServiceModelSerializer(request_services, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_request = Request.objects.get(id=kwargs.get('request_id'))
        current_service = Service.objects.get(id=kwargs.get('service_id'))
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_relation = RequestService.objects.create(request=current_request, service=current_service,
                                                     **serializer.validated_data)

        return Response(RequestServiceModelSerializer(new_relation).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        current_request = Request.objects.get(id=kwargs.get('request_id'))
        current_service = Service.objects.get(id=kwargs.get('service_id'))
        request_service = get_object_or_404(RequestService, request=current_request, service=current_service)

        request_service.trashed = True
        request_service.trashed_at = datetime.now()
        request_service.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.filter(trashed=False)
    serializer_class = CaseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_case = Case.objects.create(**serializer.validated_data)
        return Response(self.serializer_class(new_case).data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        current_case = get_object_or_404(Case, id=kwargs.get('pk'))
        current_case.trashed = True
        current_case.trashed_at = datetime.now()
        current_case.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CaseRequirementViewSet(viewsets.ModelViewSet):
    queryset = CaseRequirement.objects.filter(trashed=False)
    serializer_class = CaseRequirementSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        current_case = Case.objects.get(id=kwargs.get('case_id'), trashed=False)
        case_reqs = CaseRequirement.objects.filter(case=current_case, trashed=False)
        return Response(self.serializer_class(case_reqs, many=True).data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        current_case = Case.objects.get(id=kwargs.get('case_id'), trashed=False)
        current_req = Requirement.objects.get(id=kwargs.get('req_id'))
        obj = CaseRequirement.objects.filter(case=current_case, requirement=current_req, trashed=False)
        if len(obj) != 0:
            return Response({'detail': 'case already have the requirement called {}'.format(current_req.name)},
                            status=status.HTTP_409_CONFLICT)
        CaseRequirement.objects.create(case=current_case, requirement=current_req)
        return Response({'detail': 'Requirement Added'}, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, *args, **kwargs):
        current_case = Case.objects.get(id=kwargs.get('case_id'), trashed=False)
        current_req = Requirement.objects.get(id=kwargs.get('req_id'))
        obj = CaseRequirement.objects.filter(case=current_case, requirement=current_req, trashed=False)
        if len(obj) == 0:
            return Response({'detail': 'case does not have the requirement called {}'.format(current_req.name)},
                            status=status.HTTP_409_CONFLICT)
        case_req = obj[0]
        case_req.trashed = True
        case_req.trashed_at = datetime.now()
        case_req.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
