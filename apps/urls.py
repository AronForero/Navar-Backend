from django.urls import path, include
from apps.views import RequirementViewSet, ServiceViewSet, RequestViewSet, AuthorizeRequest, RequestCommentViewSet, \
    RequestServiceViewSet, CaseViewSet, CaseRequirementViewSet

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

comment_ops = RequestCommentViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
})

request_service_ops = RequestServiceViewSet.as_view({
    'post': 'create',
    'delete': 'destroy',
})

request_service_basic_ops = RequestServiceViewSet.as_view({
    'get': 'retrieve',
})

case_ops = CaseViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

update_case_ops = CaseViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

case_req_basic_ops = CaseRequirementViewSet.as_view({
    'get': 'retrieve',
})

case_req_ops = CaseRequirementViewSet.as_view({
    'post': 'create',
    'delete': 'destroy'
})

urlpatterns = [
    path('requirements', req_basic_ops, name='req_basic_ops'),
    path('requirements/<int:pk>', req_ops, name='req_ops'),

    path('service', service_basic_ops, name='service_basic_ops'),
    path('service/<int:pk>', service_ops, name='service_ops'),

    path('request', request_basic_ops, name='request_basic_ops'),
    path('request/<int:pk>', request_ops, name='request_ops'),
    path('request/<int:pk>/inspect', AuthorizeRequest.as_view(), name='user_inspect_request'),
    path('request/<int:pk>/comments', comment_ops, name='comments_request'),

    path('request/<int:request_id>/service/', request_service_basic_ops, name='request_service_list'),
    path('request/<int:request_id>/service/<int:service_id>', request_service_ops, name='request_service_add_delete'),

    path('case', case_ops, name='case_ops'),
    path('case/<int:pk>', update_case_ops, name='update_delete_case'),
    path('case/<int:case_id>/requirement', case_req_basic_ops, name='retrieve_reqs'),
    path('case/<int:case_id>/requirement/<int:req_id>', case_req_ops, name='create_delete_reqs'),
]
