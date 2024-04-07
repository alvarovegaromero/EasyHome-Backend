from django.urls import path
from .views import LoginAPIView, LogoutAPIView, ProfileAPIView, RegisterAPIView, ResetPasswordAPIView
from .views import reset_password

urlpatterns = [
    path('login', LoginAPIView.as_view(), name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('register', RegisterAPIView.as_view(), name='logout'),
    path('profile', ProfileAPIView.as_view(), name='profile'),
    path('reset-password', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('reset-password-form/', reset_password, name='reset_password'),
]