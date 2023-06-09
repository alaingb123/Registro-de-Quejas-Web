from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path, include

from .views import dash, InsertarQueja, insertar_respuesta, modificarQ, eliminar_ultima_queja, buscarQ, modificarR
from .views import eliminarR, buscarR, acercaDe, vista_filtrar_quejas_sin_respuestas, ir_a_administracion, informe,grafica_atrasadas

urlpatterns = [
    path('', login_required(dash), name="dash"),
    path('filtrarSR/', vista_filtrar_quejas_sin_respuestas, name='filtrar_quejas_sin_respuestas'),
    path('ir_admin/', ir_a_administracion, name='ir_admin'),
    # Gestionar Queja
    path('insertar_queja/', InsertarQueja, name="insertar_queja"),
    path('modificarQ_with_numero/<int:numero>/', modificarQ, name='modificarQ_with_numero'),
    path('eliminar_ultima_queja/', eliminar_ultima_queja, name='eliminar_ultima_queja'),
    path('buscarQ/', buscarQ, name="buscarQ"),
    # Gestionar Respuesta
    path('insertar_respuesta/', insertar_respuesta, name='insertar_respuesta'),
    path('modificarR/<int:numero>/', modificarR, name="modificarR"),
    path('eliminarR/<int:numero>/', eliminarR, name="eliminarR"),
    path('buscarR/', buscarR, name="buscarR"),
    # Acerca De
    path('acercaDe/', acercaDe, name="acercaDe"),
    path('informe/', informe, name="informe"),
    path('quejasAtrasadas/', grafica_atrasadas, name="quejasAtrasadas"),

]