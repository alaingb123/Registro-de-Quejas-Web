from django.urls import path,include
from .views import dash,InsertarQueja,insertar_respuesta
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',login_required(dash),name="dash"),
    path('insertarQueja/',InsertarQueja,name="insertar_queja"),
    path('insertarRespuesta/',insertar_respuesta,name="insertar_respuesta"),
]
