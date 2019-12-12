from django.urls import path, include
from apps.views import RequirementViewSet, ServiceViewSet, RequestViewSet, AuthorizeRequest


req_basic_ops = RequirementViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

req_ops = RequirementViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

service_basic_ops = ServiceViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

service_ops = ServiceViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

request_basic_ops = RequestViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

request_ops = RequestViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

urlpatterns = [
    path('requirements', req_basic_ops, name='req_basic_ops'),
    path('requirements/<int:pk>', req_ops, name='req_ops'),

    path('service', service_basic_ops, name='service_basic_ops'),
    path('service/<int:pk>', service_ops, name='service_ops'),

    path('request', request_basic_ops, name='request_basic_ops'),
    path('request/<int:pk>', request_ops, name='request_ops'),
    path('request/<int:pk>/inspect', AuthorizeRequest.as_view(), name='user_inspect_request'),
]
