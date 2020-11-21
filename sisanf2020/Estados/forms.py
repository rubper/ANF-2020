from django import forms
from .models import *
from Empresa.models import *
import datetime
from django.shortcuts import get_object_or_404

def obtenerCuentas(empresaid):
    cuentas = Cuenta.objects.filter(idEmpresa=empresaid)
    listadoCuentasSalida = []
    for cuenta in cuentas:
        listadoCuentasSalida.append((cuenta.idCuenta,cuenta.nombre_cuenta))
    return tuple(listadoCuentasSalida)

def obtenerEstados(tipoEstado,empresaid):
    listadoEstadoSalida=[]
    if(tipoEstado==1):
        #Todos los balance-empresa de la empresa
        relaciones=BalanceEmpresa.objects.filter(idEmpresa=empresaid)
        #Para cada uno de los objetos balance-empresa recuperados
        for relacion in relaciones:
            #obtener el balance que se trabajará de la relación
            balanceAux=relacion.idbalance
            #
            listadoEstadoSalida.append((balanceAux.idBalance,'Balance del ' + str(balanceAux.yearEstado)))
            balanceAux=None
    else:
        relaciones=EstadoEmpresa.objects.filter(idEmpresa=empresaid)
        for relacion in relaciones:
            estadoAux=relacion.idResultado
            listadoEstadoSalida.append((estadoAux.idResultado,'Estado de Resultados del '+str(estadoAux.yearEstado)))
            estadoAux=None
    return tuple(listadoEstadoSalida)

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

class SaldoCuentaForm(forms.Form):
    tipos_estados=(
        (1,'Balance General'),
        (2,'Estado de Resultado')
    )
    empresaid=0
    tipos = forms.ChoiceField(choices=tipos_estados)
    Cuenta = forms.ChoiceField(choices=obtenerCuentas(empresaid))
    idEstado = forms.ChoiceField(choices=obtenerEstados(empresaid=empresaid, tipoEstado=obtenerEstados))
    Anio = forms.HiddenInput()
    Monto = forms.DecimalField(
        max_value=None, 
        min_value=0, 
        max_digits=11, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step':'0.01'})
    )
    def __init__(self,empresaid,*args,**kwargs):
        super(SaldoCuentaForm,self).__init__(*args,**kwargs)
        self.empresaid=empresaid