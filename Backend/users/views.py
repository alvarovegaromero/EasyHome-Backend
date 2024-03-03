from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def mostrar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios})
