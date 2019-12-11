from django.urls import path, include

from authentication.views import AdditionalUserDataViewSet, UserViewSet, UserDeleteView

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

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('users', user_ops, name='user_ops'),
    path('users/<int:user_id>', UserDeleteView.as_view(), name='delete_user'),
    path('users/me', add_user_ops, name='update_user')
]
