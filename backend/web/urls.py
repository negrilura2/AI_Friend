from django.contrib.auth.views import LogoutView
from django.urls import path
from web.views.index import index
from web.views.user.account.login import LoginView
from web.views.user.account.refresh_token import RefreshTokenView
from web.views.user.account.register import RegisterView

urlpatterns = [
    path('api/user/account/login/', LoginView.as_view(), name='login'),
    path('api/user/account/logout/', LogoutView.as_view(), name='logout'),
    path('api/user/account/register/',RegisterView.as_view(), name='register'),
    path('api/user/account/refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('',index),
]
