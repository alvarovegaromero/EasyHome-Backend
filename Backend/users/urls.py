from django.urls import path
from .views import LoginAPIView, LogoutAPIView, ProfileAPIView, RegisterAPIView, ResetPasswordAPIView, ResetPasswordRequestAPIView
from .views import render_reset_password_page

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('register', RegisterAPIView.as_view(), name='logout'),
    path('profile', ProfileAPIView.as_view(), name='profile'),
    path('reset-password', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('reset-password-form/', render_reset_password_page, name='reset-password-form'), #Maybe cool to have with a separate url
    path('reset-password-request', ResetPasswordRequestAPIView.as_view(), name='reset-password-request'),
]