from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^users/?$', UserCreateListAPIView.as_view(), name='list-create-user'),
    re_path(r'^users/(?P<username>[\w-]+)/?$', UserDetailUpdateDeleteAPIView.as_view(), name='user-detail-update-delete'),
    re_path(r'^auth/token/?$', TokenAuthenticationView.as_view(), name='token-authentication'),
]