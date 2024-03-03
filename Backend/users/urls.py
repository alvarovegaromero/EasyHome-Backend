from django.urls import path
from . import views

urlpatterns = [
    path('', views.iniciar_sesion, name='inicio_sesion'),
]