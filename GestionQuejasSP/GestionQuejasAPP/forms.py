from django.forms import ModelForm,forms,DateTimeInput
from .models import Queja,Respuesta
from datetime import datetime

from django import forms
from .models import Queja

class QuejaForm(forms.ModelForm):
    fechaR = forms.DateTimeField(widget=DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        model = Queja
        fields = ['nombre_apellidos', 'entidadAfectada', 'modalidad' , 'via', 'procedencia', 'clasificacion', 'casoPrensa', 'fechaR']


class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = ['numero', 'responsable', 'descripcion', 'entrega', 'satisfaccion', 'conclusion', 'fechaE']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['numero'].queryset = Queja.objects.all()
        self.fields['numero'].label = 'Selecciona una queja'
        self.fields['numero'].empty_label = None


class FiltroQuejasForm(forms.Form):
    years = forms.ChoiceField(choices=[], label='Año')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        anos = Queja.objects.dates('fechaR', 'year').distinct()
        choices = [(ano.year, str(ano.year)) for ano in anos]
        self.fields['years'].choices = choices
        print(choices)


# class BuscadorQuejasForm(forms.Form):
#     nombre_apellidos = forms.CharField(required=False)
#     entidadAfectada = forms.CharField(required=False)
#     modalidad = forms.CharField(required=False)
#     via = forms.CharField(required=False)
#     procedencia = forms.CharField(required=False)
#     clasificacion = forms.CharField(required=False)
#     casoPrensa = forms.CharField(required=False)
#     fechaR_desde = forms.DateField(required=False)
#     fechaR_hasta = forms.DateField(required=False)


class ModificarRespuestaForm(forms.ModelForm):
    satisfaccion = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Respuesta
        fields = ['responsable', 'descripcion', 'entrega', 'satisfaccion', 'conclusion', 'fechaE']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fechaE'].required = False
