from django import forms
from .models import *
from Empresa.models import *

class ResultadoForm(forms.ModelForm):
    
    class Meta:
        model= EstadoDeResultado
        felds=[ 

        ]