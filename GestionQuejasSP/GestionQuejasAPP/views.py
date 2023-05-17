from django.shortcuts import render,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,get_object_or_404
from .forms import QuejaForm,RespuestaForm,FiltroQuejasForm,BuscadorQuejasForm
from .models import Queja
from datetime import datetime
from django.db.models import Q
from django.urls import reverse
from django.views.decorators.http import require_POST, require_http_methods


# Create your views here.
@login_required(login_url='login')
def dash(request):
    # Obtener el año actual
    current_year = datetime.now().year

    # Obtener el valor del campo years del formulario
    year = request.GET.get('years', current_year)

    # Filtrar las quejas por el año seleccionado en el formulario y ordenarlas por el campo de ordenamiento
    quejas = Queja.objects.filter(fechaR__year=year).order_by('orden')

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
            queja.orden = Queja.objects.count() + 1  # Establecer el orden en el siguiente número disponible
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
def modificarQ(request, numero):
    # Obtener la queja que se va a editar
    queja = get_object_or_404(Queja, id=numero)

    # Si el formulario se ha enviado
    if request.method == 'POST':
        # Obtener los datos del formulario
        form = QuejaForm(request.POST, instance=queja)

        # Si el formulario es válido, actualizar la queja en la base de datos
        if form.is_valid():
            queja = form.save()

            # Redirigir a la página de detalles de la queja actualizada
            return redirect('dash')

    # Si el formulario no se ha enviado, mostrar el formulario de edición
    else:
        form = QuejaForm(instance=queja)

    return render(request, 'editarQueja(prueba).html', {'form': form, 'queja': queja})


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

def seleccionar_queja(request):
    # Recuperar todas las quejas del año actual de la base de datos
    year = datetime.date.today().year
    quejas = Queja.objects.filter(fechaR__year=year)

    if request.method == 'POST':
        # Recuperar la queja seleccionada por el usuario
        pk = request.POST['pk']

        # Redirigir al usuario a la página de edición correspondiente
        return redirect('editar_queja', pk=pk)

    # Renderizar la lista de quejas disponibles
    return render(request, 'seleccionarQueja.html', {'quejas': quejas})


@login_required(login_url='login')
def eliminar_ultima_queja(request):
    ultima_queja = Queja.objects.last() # Obtiene la última queja
    ultima_queja.delete() # Elimina la última queja
    return redirect('dash')


@login_required(login_url='login')
def buscarQ(request):
    form = BuscadorQuejasForm(request.GET)
    quejas = Queja.objects.all()

    if form.is_valid():
        nombre_apellidos = form.cleaned_data.get('nombre_apellidos')
        entidadAfectada = form.cleaned_data.get('entidadAfectada')
        modalidad = form.cleaned_data.get('modalidad')
        via = form.cleaned_data.get('via')
        procedencia = form.cleaned_data.get('procedencia')
        clasificacion = form.cleaned_data.get('clasificacion')
        casoPrensa = form.cleaned_data.get('casoPrensa')
        fechaR_desde = form.cleaned_data.get('fechaR_desde')
        fechaR_hasta = form.cleaned_data.get('fechaR_hasta')

        if nombre_apellidos:
            quejas = quejas.filter(nombre_apellidos__icontains=nombre_apellidos)

        if entidadAfectada:
            quejas = quejas.filter(entidadAfectada__icontains=entidadAfectada)

        if modalidad:
            quejas = quejas.filter(modalidad__icontains=modalidad)

        if via:
            quejas = quejas.filter(via__icontains=via)

        if procedencia:
            quejas = quejas.filter(procedencia__icontains=procedencia)

        if clasificacion:
            quejas = quejas.filter(clasificacion__icontains=clasificacion)

        if casoPrensa:
            quejas = quejas.filter(casoPrensa__icontains=casoPrensa)

        if fechaR_desde:
            quejas = quejas.filter(fechaR__gte=fechaR_desde)

        if fechaR_hasta:
            quejas = quejas.filter(fechaR__lte=fechaR_hasta)

    context = {
        'form': form,
        'quejas': quejas
    }
    return render(request, 'buscarQueja.html', context)