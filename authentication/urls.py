"""
Authentication urls
"""
from django.urls import path, include
from authentication.views import CreateUserViewSet, UserViewSet, RoleViewSet, UserRoleViewSet

create_users = CreateUserViewSet.as_view({
    'post': 'create',
})

user_viewset = UserViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})

create_role = RoleViewSet.as_view({
    'post': 'create',
})

delete_role = RoleViewSet.as_view({
    'delete': 'destroy',
})

assign_role = UserRoleViewSet.as_view({
    'post': 'create',
})

urlpatterns = [
    path('public/users', create_users, name='create_user'),
    path('auth/users', user_viewset, name='get_update_user'),
    path('roles', create_role, name='create_role'),
    path('roles/<int:role_id>', delete_role, name='delete_role'),
    path('user/<int:user_id>/role/<int:role_id>', assign_role, name='assign_role'),
]
