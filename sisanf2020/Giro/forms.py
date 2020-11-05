from django import forms
from .models import *
from Giro.models import Ratios

class GiroForm(forms.ModelForm):
    idGiro = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control',
    'placeholder': 'Rango:[1-99]','pattern': '[0-9]+','title': 'Números únicamente','maxlength' : '2'}))
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

class DatoGiroForm(forms.ModelForm):
    class Meta:
        model = DatoGiro
        fields = [
        'idGiro',
        'idRatio',
        'valorParametro',
        'valorPromedio',
        ]
        labels = {
        'idGiro' : 'Giro',
        'idRatio' : 'Ratio',
        'valorParametro' : 'Valor parámetro',
        'valorPromedio': 'Valor promedio',
        }
        widgets = {
        'idGiro' : forms.Select(attrs={'class': 'form-control'}),
        'idRatio' : forms.Select(attrs={'class': 'form-control'}),
        'valorParametro' : forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9, .]+','title': 'Números únicamente','maxlength' : '8'}),
        'valorPromedio' : forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9, .]+','title': 'Números únicamente','maxlength' : '8'}),
        }

class UpdateDatoGiroForm(forms.ModelForm):
    class Meta:
        model = DatoGiro
        fields = [
        'idGiro',
        'idRatio',
        'valorParametro',
        'valorPromedio',
        ]
        labels = {
        'idGiro' : 'Giro',
        'idRatio' : 'Ratio',
        'valorParametro' : 'Valor parámetro',
        'valorPromedio': 'Valor promedio',
        }
        widgets = {
        'idGiro' : forms.Select(attrs={'class': 'form-control', 'disable':'True'}),
        'idRatio' : forms.Select(attrs={'class': 'form-control', 'disable':'True'}),
        'valorParametro' : forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9, .]+','title': 'Números únicamente','maxlength' : '8'}),
        'valorPromedio' : forms.TextInput(attrs={'class': 'form-control', 'pattern': '[0-9, .]+','title': 'Números únicamente','maxlength' : '8'}),
        }
