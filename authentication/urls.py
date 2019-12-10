from django.urls import path, include

from authentication.views import AdditionalUserDataViewSet, UserViewSet

user_ops = UserViewSet.as_view({
    'post': 'create',
    'get': 'retrieve',
})

add_user_ops = AdditionalUserDataViewSet.as_view({
    'post': 'create',
    'put': 'update',
    'get': 'retrieve',
})

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('users', user_ops, name='user_ops'),
    path('users/me', add_user_ops, name='update_user')
]
