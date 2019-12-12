from django.urls import path, include

from authentication.views import AdditionalUserDataViewSet, UserViewSet, UserDeleteView, RolesViewSet, UserRoleViewSet

user_ops = UserViewSet.as_view({
    'post': 'create',
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

add_user_ops = AdditionalUserDataViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'put': 'update',
})

roles_basic_ops = RolesViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

roles_other_ops = RolesViewSet.as_view({
    'put': 'update',
    'delete': 'destroy',
})

user_role_ops = UserRoleViewSet.as_view({
    'post': 'create',
    'delete': 'destroy',
})

user_role_basic_ops = UserRoleViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('users', user_ops, name='user_ops'),
    path('users/<int:user_id>', UserDeleteView.as_view(), name='delete_user'),
    path('users/me', add_user_ops, name='update_user'),
    path('roles', roles_basic_ops, name='roles_basic_ops'),
    path('roles/<int:pk>', roles_other_ops, name='roles_other_ops'),
    path('user/<int:user_id>/role/<int:role_id>', user_role_ops, name='user_role_create'),
    path('users/roles', user_role_basic_ops, name='user_roles_basic_ops'),
]
