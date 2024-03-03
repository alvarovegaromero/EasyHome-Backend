from django.shortcuts import render
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.

def iniciar_sesion(request):
    return render(request, 'usuarios.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'usuarios.html', {'login_success': True})
        else:
            return render(request, 'usuarios.html', {'login_error': True})
    else:
        return render(request, 'usuarios.html')
