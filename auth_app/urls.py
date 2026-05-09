from django.urls import path
from .views import login_user
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login-token/", login_user, name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
