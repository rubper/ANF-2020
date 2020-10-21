from django import forms
from .models import *

class GiroForm(forms.ModelForm):
    idGiro = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control',
    'placeholder': 'Rango:[1-99]','pattern': '[1-99]+','title': 'Números únicamente','maxlength' : '2'}))
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
        #'idGiro' : forms.NumberInput(attrs={'class': 'form-control'}),
        'nombreGiro' : forms.TextInput(attrs={'class': 'form-control'}),
        'sector' : forms.Select(attrs={'class': 'form-control'}),
        }

class UpdateGiroForm(forms.ModelForm):
    idGiro= forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'True'}))
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
        #'idGiro' : forms.NumberInput(attrs={'class': 'form-control'}),
        'nombreGiro' : forms.TextInput(attrs={'class': 'form-control'}),
        'sector' : forms.Select(attrs={'class': 'form-control'}),
        }
