from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import QuejaForm
from .models import Queja


# Create your views here.
@login_required(login_url='login')
def dash(request):
    return render(request,'dashboard/dash.html')



def InsertarQueja(request):
    if request.method == 'POST':
        form = QuejaForm(request.POST)
        if form.is_valid():
            queja = form.save(commit=False)
            # Modificar el modelo queja si es necesario
            queja.save()
            # El formulario es válido, guardar los datos en la base de datos
            return render(request, 'dashboard/dash.html')
    else:
        error_message='Datos Invalidos'
    return render(request, 'insertarQueja.html', {'error_message': error_message})