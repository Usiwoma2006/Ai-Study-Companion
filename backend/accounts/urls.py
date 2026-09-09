from django.urls import path, include
from accounts.views import LoginView, SignupView, GoogleLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("", include("dj_rest_auth.urls")),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("google/", GoogleLoginView.as_view(), name="google_login"),
]