from django import forms
from Giros.models import *

class GiroForm(forms.ModelForm):
    class Meta:
        model = Giro
        fields = [
        'nombreGiro',
        'sector',
        ]
        labels = {
        'nombreGiro' : 'Nombre',
        'sector' : 'Sector',
        }
        widgets = {
        'nombreGiro' : forms.TextInput(attrs={'class': 'form-control'}),
        'sector' : forms.TextInput(attrs={'class': 'form-control'}),
        }
