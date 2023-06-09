from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import QuejaForm, RespuestaForm, FiltroQuejasForm, ModificarRespuestaForm
from .models import Queja, Respuesta
from django.shortcuts import render
from django.db.models import Count, Case, When, IntegerField
from datetime import datetime, timedelta
import json
from django.utils.dateformat import DateFormat
from django.utils import timezone



# Create your views here.
@login_required
def user_in_group(request):
    usuario = request.user
    group = Group.objects.get(name='Funcionario')
    return True if group in usuario.groups.all() else False


@login_required
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


# Gestionar Queja


@user_passes_test(user_in_group, login_url='')
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

# def InsertarQueja(request):
#     error_message = ''
#     if request.method == 'POST':
#         form = QuejaForm(request.POST)
#         if form.is_valid():
#             queja = form.save(commit=False)
#             queja.orden = Queja.objects.count() + 1  # Establecer el orden en el siguiente número disponible
#             queja.save()
#             # El formulario es válido, guardar los datos en la base de datos
#             return redirect(reverse('dash'))
#         else:
#             error_message = 'Datos inválidos, verifique el formulario'
#     else:
#         form = QuejaForm()
#     return render(request, 'Gestionar Queja/insertarQ.html', {'form': form, 'error_message': error_message})


@user_passes_test(user_in_group, login_url='')
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

    return render(request, 'Gestionar Queja/editarQueja.html', {'form': form, 'queja': queja})


@login_required
def buscarQ(request):
    quejas = None
    if request.GET:
        nombre_apellidos = request.GET.get('nombre_apellidos')
        entidadAfectada = request.GET.get('entidadAfectada')
        modalidad = request.GET.get('modalidad')
        via = request.GET.get('via')
        procedencia = request.GET.get('procedencia')
        clasificacion = request.GET.get('clasificacion')
        casoPrensa = request.GET.get('casoPrensa')
        fechaR_desde = request.GET.get('fechaR_desde')
        fechaR_hasta = request.GET.get('fechaR_hasta')
        numero = request.GET.get('numero')

        quejas = Queja.objects.all()

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

        if numero:
            quejas = quejas.filter(numero__icontains=numero)

    return render(request, 'Gestionar Queja/buscarQueja.html', {'quejas': quejas})


@user_passes_test(user_in_group, login_url='')
def eliminar_ultima_queja(request):
    ultima_queja = Queja.objects.last()  # Obtiene la última queja
    ultima_queja.delete()  # Elimina la última queja
    return redirect('dash')


# Gestionar Respuesta

@user_passes_test(user_in_group, login_url='')
def insertar_respuesta(request):
    # Obtener el año actual
    current_year = datetime.now().year

    # Filtrar las quejas sin respuesta y por año
    quejas = Queja.objects.filter(respuesta__isnull=True, fechaR__year=current_year)

    if request.method == 'POST':
        form = ModificarRespuestaForm(request.POST)
        if form.is_valid():
            # Guardar la respuesta nueva
            respuesta = form.save(commit=False)
            respuesta.save()
            return redirect('dash')
    else:
        form = RespuestaForm()

    context = {
        'quejas': quejas,
        'form': form,
    }
    return render(request, 'Gestionar Respuesta/insertarRespuesta.html', context)


@user_passes_test(user_in_group, login_url='')
def modificarR(request, numero):
    respuesta = get_object_or_404(Respuesta, numero_id=numero)
    if request.method == 'POST':
        form = ModificarRespuestaForm(request.POST, instance=respuesta)
        if form.is_valid():
            form.save()
            return redirect('dash')
        else:
            # Agregar mensajes de error a la variable 'messages'
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RespuestaForm(instance=respuesta)
    return render(request, 'Gestionar Respuesta/modificarRespuesta.html', {'form': form, 'respuesta': respuesta})


@user_passes_test(user_in_group, login_url='')
def eliminarR(request, numero):
    # Buscamos la respuesta por su número
    respuesta = get_object_or_404(Respuesta, numero=numero)

    if request.method == 'POST':
        # Si se ha enviado el formulario de confirmación, eliminamos la respuesta
        respuesta.delete()
        # Redirigimos a otra página, por ejemplo la lista de quejas
        return redirect('dash')


def buscarR(request):
    resultados = Respuesta.objects.all()

    if 'numero' in request.GET and request.GET['numero']:
        numero = request.GET['numero']
        resultados = resultados.filter(numero__numero__icontains=numero)

    if 'responsable' in request.GET and request.GET['responsable']:
        responsable = request.GET['responsable']
        resultados = resultados.filter(responsable__icontains=responsable)

    if 'descripcion' in request.GET and request.GET['descripcion']:
        descripcion = request.GET['descripcion']
        resultados = resultados.filter(descripcion__icontains=descripcion)

    if 'entrega' in request.GET and request.GET['entrega']:
        entrega = request.GET['entrega']
        resultados = resultados.filter(entregado__icontains=entrega)

    if 'satisfaccion' in request.GET and request.GET['satisfaccion']:
        satisfaccion = request.GET['satisfaccion']
        resultados = resultados.filter(satisfaccion__icontains=satisfaccion)

    if 'conclusion' in request.GET and request.GET['conclusion']:
        conclusion = request.GET['conclusion']
        resultados = resultados.filter(conclusiones__icontains=conclusion)

    if 'fechaE' in request.GET and request.GET['fechaE']:
        fechaE = request.GET['fechaE']
        resultados = resultados.filter(fecha_entrega__icontains=fechaE)

    # Combinar los filtros con Q para permitir búsquedas en varios campos
    # de forma opcional
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        resultados = resultados.filter(
            Q(numero__numero__icontains=q) |
            Q(responsable__icontains=q) |
            Q(descripcion__icontains=q) |
            Q(entregado__icontains=q) |
            Q(satisfaccion__icontains=q) |
            Q(conclusiones__icontains=q) |
            Q(fecha_entrega__icontains=q)
        )

    return render(request, 'Gestionar Respuesta/BuscarRespuesta.html', {'resultados': resultados})


# Otras


@login_required
def vista_filtrar_quejas_sin_respuestas(request):
    form = FiltroQuejasForm(request.GET or None)
    queja_id = None

    if form.is_valid():
        year = form.cleaned_data['years']
        fecha = form.cleaned_data['fecha']
        quejas = Queja.objects.exclude(
            Q(respuesta__isnull=False) | Q(respuesta__exact='')
        )

        if year:
            quejas = quejas.filter(fechaR__year=year)

        if fecha:
            quejas = quejas.filter(fechaR__date=fecha)

    else:
        quejas = Queja.objects.exclude(
            Q(respuesta__isnull=False) | Q(respuesta__exact='')
        )

    context = {
        'form': form,
        'quejas': quejas,
        'queja_id': queja_id,
    }

    return render(request, 'Gestionar Respuesta/insertarRespuesta.html', context)


@login_required
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


@login_required
def acercaDe(request):
    return render(request, 'acerca de.html')


def ir_a_administracion(request):
    return redirect(reverse('admin:index'))


# def ValidacionPermisoRequeridMixi():
#     def dispacht (self,r)

def informe(request):
    # Obtener la lista de entidades afectadas y meses únicos
    entidades = Queja.objects.values_list('entidadAfectada', flat=True).distinct().order_by('entidadAfectada')
    meses = Queja.objects.annotate(mes=TruncMonth('fechaR')).values_list('mes', flat=True).distinct().order_by('mes')

    # Crear una matriz para los valores de la gráfica
    valores = []
    for mes in meses:
        fila = [0] * len(entidades)
        for i, entidad in enumerate(entidades):
            quejas = Queja.objects.filter(fechaR__month=mes.month, fechaR__year=mes.year, entidadAfectada=entidad)
            cantidad = quejas.count()
            fila[i] = cantidad
        valores.append(fila)
    print(entidades)
    print(meses)
    print(valores)
    # Pasar los datos a la plantilla
    return render(request, 'Gestionar Queja/resumen.html', {
        'entidades': entidades,
        'meses': meses,
        'valores': valores,
    })

def grafica_atrasadas(request):
    # Obtener fecha actual
    fecha_actual = datetime.now(timezone.utc).date()

    # Obtener la lista de entidades afectadas y meses únicos
    entidades = Queja.objects.values_list('entidadAfectada', flat=True).distinct().order_by('entidadAfectada')
    meses = Queja.objects.filter(fechaT__lt=fecha_actual, respuesta__isnull=True).annotate(mes=TruncMonth('fechaR')).values_list('mes', flat=True).distinct().order_by('mes')

    # Crear una matriz para los valores de la gráfica
    valores = []
    for mes in meses:
        fila = [0] * len(entidades)
        for i, entidad in enumerate(entidades):
            quejas = Queja.objects.filter(fechaR__month=mes.month, fechaR__year=mes.year, entidadAfectada=entidad, respuesta__isnull=True, fechaT__lt=fecha_actual)
            cantidad = quejas.count()
            fila[i] = cantidad
        valores.append(fila)

    # Obtener la lista de quejas atrasadas
    quejas_atrasadas = Queja.objects.filter(fechaT__lt=fecha_actual, respuesta__isnull=True)
    print(quejas_atrasadas)
    # Pasar los datos a la plantilla
    return render(request, 'Gestionar Queja/quejasAtrasadas.html', {
        'entidades': entidades,
        'meses': meses,
        'valores': valores,
        'quejas_atrasadas': quejas_atrasadas,
    })