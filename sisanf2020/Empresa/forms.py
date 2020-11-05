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



#class CuentaFormd(forms.ModelForm):
#   class Meta:
#       models=Cuenta,SaldoDeCuenta
#       fields=[
#
#        ]
