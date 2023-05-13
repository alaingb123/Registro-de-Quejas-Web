from django.urls import path,include
from .views import dash
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('dash/',login_required(dash),name="dash"),
]
