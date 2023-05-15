from django.urls import path,include
from .views import dash,InsertarQueja
from django.contrib.auth.decorators import login_required
from .views import dash,insertarQ

urlpatterns = [
    path('',login_required(dash),name="dash"),
    path('insertar/',insertarQ,name="insertarQ"),
]
