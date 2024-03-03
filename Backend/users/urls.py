from django.urls import path
from .views import mostrar_usuarios

urlpatterns = [
    path('', mostrar_usuarios, name='mostrar_usuarios'),
]