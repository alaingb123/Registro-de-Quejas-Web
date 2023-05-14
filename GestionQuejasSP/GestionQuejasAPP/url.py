from django.urls import path,include
from .views import dash,InsertarQueja
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',login_required(dash),name="dash"),
    path('insertarQueja/',InsertarQueja,name="insertar"),
]
