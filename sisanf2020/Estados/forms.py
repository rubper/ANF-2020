from django import forms
from .models import *
from Empresa.models import *
import datetime

class EstadoForm(forms.Form):
    moneda_codigo=(
        ('USD','Dolares estadounodense'),
        ('SVC','Colón salvadoreño'),
        ('EUR','Euro'),
    )
    fechaInicioBalance = forms.DateField(widget=forms.DateInput(attrs={'type':'date','max':datetime.datetime.now().strftime('%Y-%m-%d'), 'value':datetime.datetime.now().strftime('%Y-%m-%d')}))
    fechaFinBalance = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'min':fechaInicioBalance, 'value':datetime.datetime.now().strftime('%Y-%m-%d')}))
    yearEstado = forms.IntegerField(initial=datetime.datetime.now().year)
    moneda_codigo_balance = forms.ChoiceField(choices=moneda_codigo,required=True)