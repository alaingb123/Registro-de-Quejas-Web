from django.urls import path,include
from .views import dash,InsertarQueja,insertar_respuesta,modificarQ,eliminarQ,buscarQ,modificarR,eliminarR,buscarR,acercaDe
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',login_required(dash),name="dash"),
    #Gestionar Queja
    path('insertar_queja/', InsertarQueja, name="insertar_queja"),
    path('modificarQ/',modificarQ,name="modificarQ"),
    path('eliminarQ/',eliminarQ,name="eliminarQ"),
    path('buscarQ/',buscarQ,name="buscarQ"),
    #Gestionar Respuesta
    path('insertar_respuesta/',insertar_respuesta,name="insertar_respuesta"),
    path('modificarR/', modificarR, name="modificarR"),
    path('eliminarR/', eliminarR, name="eliminarR"),
    path('buscarR/', buscarR, name="buscarR"),
    #Acerca De
    path('acercaDe/', acercaDe, name="acercaDe"),
]
