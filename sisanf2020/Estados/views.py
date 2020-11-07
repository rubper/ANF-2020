from django.shortcuts import render
from Empresa.models import Cuenta, SaldoDeCuentaResultado, EstadoEmpresa
from Estados.models import EstadoDeResultado

# Create your views here.
def indexEstadoResultado(request, empresa, anio):
    #Obtengo todas las cuentas de la empresa
    Cuentas = Cuenta.objects.filter(idEmpresa=empresa).order_by('idCuenta')
    #Obtengo todos los estados de resultado de la empresa (tengo los idResultado)
    EstadosEmpresa = EstadoEmpresa.objects.filter(idEmpresa=empresa).order_by('idResultado')
    #Obtengo el estado del anio dado    
    Resultados = []
    #Para cada estado de la empresa
    for estado in EstadosEmpresa:
        #Si el estado es del año dado
        if(estado.idResultado.yearEstado==anio):
            #Añadir a Estados de Resultados del año
            Resultados.append(estado.idResultado)
    #Obtengo todos los saldos con los estados
    SaldosCuentasEmpresa = []
    #Para cada cuenta de la empresa
    for cuenta in Cuentas:
        #Añadir a Listado de saldo de cuentas, los saldos de cuentas correspondientes al listado de cuentas
        SaldosCuentasEmpresa.append(SaldoDeCuentaResultado.objects.filter(idCuenta=cuenta.idCuenta).first())
        #Se tienen todos los saldos de cuentas relacionados a las cuentas de la empresa
    #Obtengo los saldos del estado de resultado
    SaldoEstado = []
    if(len(Resultados)>0):
        ResultadoActual = Resultados[0]
        #Para cada saldo de las cuentas de la empresa
        for saldoEmpresa in SaldosCuentasEmpresa:
            if(saldoEmpresa.year_saldo_Resul.year == ResultadoActual.yearEstado):
                #Añadir a los Saldos del estado de resultado del mismo anio
                SaldoEstado.append(saldoEmpresa)
    argumentos = {
        'salidaDebug1':Cuentas,
        'salidaDebug2':SaldosCuentasEmpresa,
        'salidaDebug3':SaldoEstado,
        'salidaDebug4':Resultados,
    }
    return render(request,'Estados/EstadoResultados.html', argumentos)