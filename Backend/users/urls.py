from django.urls import path
from . import views

urlpatterns = [
    path('api/login', views.LoginAPIView.as_view(), name='login'),
    path('api/logout', views.LogoutAPIView.as_view(), name='logout'),
]