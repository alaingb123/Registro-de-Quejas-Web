from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import QuejaForm,RespuestaForm,FiltroQuejasForm
from .models import Queja
from django.views.decorators.cache import never_cache
from datetime import datetime
from django.db.models import Q
from django.urls import reverse


# Create your views here.
@login_required(login_url='login')
def dash(request):
    # Obtener el año actual
    current_year = datetime.now().year

    # Obtener el valor del campo years del formulario
    year = request.GET.get('years', current_year)

    # Filtrar las quejas por el año seleccionado en el formulario
    quejas = Queja.objects.filter(fechaR__year=year)

    # Inicializar el formulario con el valor seleccionado en el formulario
    form = FiltroQuejasForm(initial={'years': year})

    context = {
        'form': form,
        'quejas': quejas,
    }

    # Renderizar la plantilla y devolver una respuesta HttpResponse que contenga el objeto de contexto
    return render(request, 'dashboard/dash.html', context)


@login_required(login_url='login')
def InsertarQueja(request):
    error_message = ''
    if request.method == 'POST':
        form = QuejaForm(request.POST)
        if form.is_valid():
            queja = form.save(commit=False)
            # Modificar el modelo queja si es necesario
            queja.save()
            # El formulario es válido, guardar los datos en la base de datos
            return redirect(reverse('dash'))
        else:
            error_message = 'Datos inválidos, verifique el formulario'
    else:
        form = QuejaForm()
    return render(request, 'Gestionar Queja/insertarQ.html', {'form': form, 'error_message': error_message})

@login_required(login_url='login')
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
@login_required(login_url='login')
def modificarQ(request):
    return render(request,'Gestionar Queja/editarQueja.html')
@login_required(login_url='login')
def eliminarQ(request):
    return render(request,'Gestionar Queja/eliminarQueja.html')

@login_required(login_url='login')
def buscarQ(request):
    return render(request,'Gestionar Queja/buscarQueja.html')
@login_required(login_url='login')
def modificarR(request):
    return render(request,'Gestionar Respuesta/modificarRespuesta.html')
@login_required(login_url='login')
def eliminarR(request):
    return render(request,'Gestionar Respuesta/eliminarRespuesta.html')
@login_required(login_url='login')
def buscarR(request):
    return render(request,'Gestionar Respuesta/BuscarRespuesta.html')
@login_required(login_url='login')
def acercaDe(request):
    return render(request,'acerca de.html')




def vista_filtrar_quejas_sin_respuestas(request):
    form = FiltroQuejasForm(request.GET or None)

    if form.is_valid():
        year = form.cleaned_data['years']
        quejas = Queja.objects.filter(fechaR__year=year).exclude(
            Q(respuesta__isnull=False) | Q(respuesta__exact='')
        )
    else:
        quejas = Queja.objects.exclude(
            Q(respuesta__isnull=False) | Q(respuesta__exact='')
        )

    context = {
        'form': form,
        'quejas': quejas,
    }

    return render(request, 'dashboard/dash.html', context)