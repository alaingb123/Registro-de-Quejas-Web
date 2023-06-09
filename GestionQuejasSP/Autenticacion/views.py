from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect


def logear(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dash')
        else:
            error_message = 'Credenciales Invalidas'
    else:
        error_message = None
    return render(request, 'Autenticacion/login.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('autenticacion')