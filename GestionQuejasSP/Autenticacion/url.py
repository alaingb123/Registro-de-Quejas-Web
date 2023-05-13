from Autenticacion import views
from django.urls import path
from .views import logear,cerrar_sesion



urlpatterns = [

path('',logear,name="autenticacion"),
path('cerrar_sesion',cerrar_sesion,name="cerrar_sesion"),

]