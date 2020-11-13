from django import forms
from .models import *

class Empresa_Forms(forms.ModelForm):
    class Meta:
        model = Empresa
        fields=[
            'idEmpresa',
            'idGiro',
            'rasonsocial',
            'telefono',
            'nrc',
            'nit',
            'direccion',
        ]
        labels={
            'idEmpresa' :'id',
            'idGiro': 'Giro',
            'rasonsocial': 'rasonsocial',
            'telefono': 'telefono',
            'nrc':'NCR',
            'nit':'NIT',
            'direccion':'direccion',
        }

        widgets = {
            'idEmpresa': forms.TextInput(attrs={'class': 'form-control'}),
            'idGiro':forms.Select(attrs={'class': 'form-control'}),
            'rasonsocial':forms.TextInput(attrs={'class': 'form-control'}),
            'telefono':forms.TextInput(attrs={'class': 'form-control'}),
            'nrc':forms.TextInput(attrs={'class': 'form-control'}),
            'nit':forms.TextInput(attrs={'class': 'form-control'}),
            'direccion':forms.TextInput(attrs={'class': 'form-control'}),
        }


class CuentaFor(forms.ModelForm):
   class Meta:
        model= Cuenta
        fields=[
           'idCuenta',
           'idEmpresa',
           'codigo_cuenta',
           'nombre_cuenta',
           'tipo_cuenta',
           'naturaleza_cuenta',
        ]
        labels = {
           'idCuenta':'id',
           'idEmpresa':'empresa',
           'codigo_cuenta':'codigo',
           'nombre_cuenta':'cuenta',
           'tipo_cuenta':'tipo',
           'naturaleza_cuenta':'narturaleza',
        }
        widgets = {
           'idCuenta':forms.TextInput(attrs={'class':'form-control'}),
           'idEmpresa':forms.Select(attrs={'class':'form-control'}),
           'codigo_cuenta':forms.TextInput(attrs={'class':'form-control'}),
           'nombre_cuenta':forms.TextInput(attrs={'class':'form-control'}),
           'tipo_cuenta':forms.Select(attrs={'class':'form-control'}),
           'naturaleza_cuenta':forms.Select(attrs={'class':'form-control'}),
        }

class CuentaForm(forms.Form):
    tipo=(
        ('Activo Corrinte','Activo Corrinte'),
        ('Activo no Corrinte','Activo no Corrinte'),
        ('Pasivo Corrinte','Pasivo Corrinte'),
        ('Pasivo no Corrinte','Pasivo no Corrinte'),
        ('Capital','Capital'),
        ('Estado de Resultado','Estado de Resultado'),
    )
    naturaleza=(
        ('Acreedor','Acreedor'),
        ('Deudor','Deudor'), 
    )
    codigo_cuenta = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), max_length=13)
    nombre_cuenta = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    tipo_cuenta = forms.ChoiceField(choices=tipo,required=True,widget=forms.Select(attrs={'class':'form-control'}))
    naturaleza_cuenta = forms.ChoiceField(choices=naturaleza,required=True,widget=forms.Select(attrs={'class':'form-control'}))
