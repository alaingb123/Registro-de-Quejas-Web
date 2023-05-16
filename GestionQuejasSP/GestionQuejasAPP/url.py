from django.urls import path,include
from .views import dash,InsertarQueja,insertar_respuesta,modificarQ,eliminar_ultima_queja,buscarQ,modificarR,eliminarR,buscarR,acercaDe,vista_filtrar_quejas_sin_respuestas
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',login_required(dash),name="dash"),
    path('filtrarSR/', vista_filtrar_quejas_sin_respuestas, name='filtrar_quejas_sin_respuestas'),
    #Gestionar Queja
    path('insertar_queja/', InsertarQueja, name="insertar_queja"),
    path('modificarQ/<int:pk>/', modificarQ, name='modificarQ_with_numero'),
    path('modificarQ/', modificarQ, name='modificarQ'),
    path('eliminar_ultima_queja/', eliminar_ultima_queja, name='eliminar_ultima_queja'),
    path('buscarQ/',buscarQ,name="buscarQ"),
    #Gestionar Respuesta
    path('insertar_respuesta/',insertar_respuesta,name="insertar_respuesta"),
    path('modificarR/', modificarR, name="modificarR"),
    path('eliminarR/', eliminarR, name="eliminarR"),
    path('buscarR/', buscarR, name="buscarR"),
    #Acerca De
    path('acercaDe/', acercaDe, name="acercaDe"),



]
