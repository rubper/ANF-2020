from django import forms
from .models import *

class GiroForm(forms.ModelForm):
    class Meta:
        model = Giro
        fields = [
        'idGiro',
        'nombreGiro',
        'sector',
        ]
        labels = {
        'idGiro' : 'Id',
        'nombreGiro' : 'Nombre',
        'sector' : 'Sector',
        }
        widgets = {
        'idGiro' : forms.NumberInput(attrs={'class': 'form-control'}),
        'nombreGiro' : forms.TextInput(attrs={'class': 'form-control'}),
        'sector' : forms.Select(attrs={'class': 'form-control'}),
        }
