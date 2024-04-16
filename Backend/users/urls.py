from django.urls import path
from .views.login.LoginAPIView import LoginAPIView
from .views.logout.LogoutAPIView import LogoutAPIView
from .views.profile.ProfileAPIView import ProfileAPIView
from .views.register.RegisterAPIView import RegisterAPIView
from .views.reset_password.ResetPasswordAPIView import ResetPasswordAPIView
from .views.reset_password.ResetPasswordRequestAPIView import ResetPasswordRequestAPIView
from django.shortcuts import render

def render_reset_password_page(request):
    return render(request, 'password_reset.html')

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('register', RegisterAPIView.as_view(), name='register'),
    path('profile', ProfileAPIView.as_view(), name='profile'),
    path('reset-password', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('reset-password-form/', render_reset_password_page, name='reset-password-form'), #Maybe cool to have with a separate url
    path('reset-password-request', ResetPasswordRequestAPIView.as_view(), name='reset-password-request'),
]