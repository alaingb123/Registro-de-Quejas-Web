from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import QuejaForm,RespuestaForm
from .models import Queja
from django.views.decorators.cache import never_cache
from datetime import datetime


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
    return render(request, 'Gestionar Queja/insertarQ.html', {'error_message': error_message})


def insertar_respuesta(request):
    if request.method == 'POST':
        form = RespuestaForm(request.POST)
        if form.is_valid():
            respuesta = form.save(commit=False)
            queja_id = form.cleaned_data['numero'].id
            respuesta.queja = Queja.objects.get(id=queja_id)
            respuesta.save()
            # hacer algo después de guardar la respuesta
            return redirect('dash')
        else:
            print(form.errors)  # mostrar errores de validación del formulario
    else:
        form = RespuestaForm()
    return render(request, 'InsertarRespuesta.html', {'form': form})