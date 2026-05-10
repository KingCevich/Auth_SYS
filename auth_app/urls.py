from django.urls import path
from .views import login_user, validate_token
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login-token/", login_user, name="login"),
    path("validate-token/", validate_token, name="validate_token"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
