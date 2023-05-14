from django.forms import ModelForm,forms
from .models import Queja

from django import forms
from .models import Queja

class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['nombre_apellidos', 'entidadAfectada', 'modalidad' , 'via', 'procedencia', 'clasificacion', 'casoPrensa', 'fechaR']



