from django.urls import path
from . import views

urlpatterns = [
    path('inicio-sesion/', views.iniciar_sesion, name='inicio_sesion'),
    path('login/', views.login_view, name='login'),
]