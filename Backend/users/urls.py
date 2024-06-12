from django.shortcuts import render
from django.urls import path

from .views.email_verification.email_verification_view import EmailVerificationAPIView
from .views.login.login_view import LoginAPIView
from .views.logout.logout_view import LogoutAPIView
from .views.my_info_token_view import MyInfoTokenAPIView
from .views.profile.profile_view import ProfileAPIView
from .views.register.register_view import RegisterAPIView
from .views.reset_password.reset_password_request_view import (
    ResetPasswordRequestAPIView,
)
from .views.reset_password.reset_password_view import ResetPasswordAPIView


# didn't know where to place. maybe inside a view?
def render_reset_password_page(request):
    return render(request, "password_reset.html")


urlpatterns = [
    path("login", LoginAPIView.as_view(), name="login"),
    path("logout", LogoutAPIView.as_view(), name="logout"),
    path("register", RegisterAPIView.as_view(), name="register"),
    path("profile", ProfileAPIView.as_view(), name="profile"),
    path("reset-password", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("reset-password-form/", render_reset_password_page, name="reset-password-form"),
    # Maybe cool to have with a separate url
    path(
        "reset-password-request",
        ResetPasswordRequestAPIView.as_view(),
        name="reset-password-request",
    ),
    path("email-verification", EmailVerificationAPIView.as_view(), name="email-verification"),
    path("my-info", MyInfoTokenAPIView.as_view(), name="my-info"),
]
