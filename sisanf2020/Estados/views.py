from django.shortcuts import render
from Empresa.models import Cuenta, SaldoDeCuentaResultado, EstadoEmpresa, Empresa
from Estados.models import EstadoDeResultado
from Estados.resources import EstadoResource
from tablib import Databook, Dataset
from django.contrib import messages
from datetime import datetime

def indexEstados(request, empresa):
    #se ejecuta solo cuando la request es post
    if request.method == 'POST':
        ########Obtener variables para procesos##########
        #obtener del ultimo saldo registrado en la base
        Saldoultimo = SaldoDeCuentaResultado.objects.latest('idSaldoResul')
        #Obtener todas las relaciones estado/empresa que corresponden a la empresa actual
        RelacionesEstadoEmpresa = EstadoEmpresa.objects.filter(idEmpresa=empresa)
        #Declara variable IdDelEstado como None (Para asegurar que será None en caso que falle proc)
        IdDelEstado = None

        #######Inicia proceso########
        #obtener el archivo de la request
        archivo = request.FILES['subirEstados']
        #si el archivo no es xlsx
        if not archivo.name.endswith('xlsx'):
            #mostrar error
            messages.error(request,'Error: Formato incorrecto')  
            return render(request)  
        #crear instancia tablib Dataset
        conjuntoDatos = Dataset()
        #Definir headers del dataset
        #Estos son los headers que debe tener la tabla de excel
        conjuntoDatos.headers = ('Codigo de Cuenta', 'Nombre de la cuenta', 'Anio del Estado', 'Monto')
        #cargar el archivo de la request en la instancia Dataset
        datosImportados = conjuntoDatos.load(archivo.read(),format='xlsx')
        #obtener el id del ultimo saldo de estado ingresado
        idSaldoUltimo = Saldoultimo.idSaldoResul
        #ciclo con el archivo cargado en la instancia dataset
        #para cada registro en los datos importados
        for registro in datosImportados:   
            #aumentar 1 al id
            idSaldoUltimo += 1
            #para cada estado de la empresa
            for estadoempresa in RelacionesEstadoEmpresa:
                #si el anio del estado actual corresponde a la tercera columna de los datos importados
                #(La columna deben ser los años)
                if(estadoempresa.idResultado.yearEstado==registro[2]):
                    #almacenar el id del estado
                    IdDelEstado = estadoempresa.idResultado.idResultado
            #Si al final del ciclo no se encuentra, levantar mensaje de error
            #(Falta escribir un try-catch que capture la excepción y muestre mensaje de que no existe el estado)
            if(IdDelEstado==None):
                raise TypeError("No existe el estado de resultado")
            #Se obtiene la cuenta con el id de la empresa y el codigo
            #(El codigo de la cuenta proviene de la primera columna del excel)
            cuentaObtenida = Cuenta.objects.get(idEmpresa=empresa,codigo_cuenta=registro[0])
            #instancia del modelo de SaldoDeCuentaResultado
            valor = SaldoDeCuentaResultado(
                #1. id
                idSaldoUltimo,
                #2. idcuenta
                cuentaObtenida.idCuenta,
                #3. idresultado
                IdDelEstado,
                #4. año
                datetime(registro[2],1,1),
                #5. monto
                registro[3]
            )
            #ejecutar insert
            valor.save()


    return render(request, 'Estados/EstadosIndex.html')

# Create your views here.
def indexEstadoResultado(request, empresa, anio):
    ##################OBTENER TODAS LAS CUENTAS DE LA EMPRESA##########################
    #Obtengo todas las cuentas de la empresa
    Cuentas = Cuenta.objects.filter(idEmpresa=empresa).order_by('idCuenta')
    
    ##################OBTENER LA EMPRESA#############################
    EmpresaActual = Empresa.objects.get(idEmpresa=empresa)

    ##################OBTENER TODOS LOS ESTADOS DE LA EMPRESA##########################
    #Obtengo todos los estados de resultado de la empresa (tengo los idResultado)
    EstadosEmpresa = EstadoEmpresa.objects.filter(idEmpresa=empresa).order_by('idResultado')
    #Obtengo el estado del anio dado    
    Resultados = []
    Anios = []
    #Para cada estado de la empresa
    for estado in EstadosEmpresa:
        #Si el estado es del año dado
        if(estado.idResultado.yearEstado==anio):
            #Añadir a Estados de Resultados del año
            Resultados.append(estado.idResultado)
        #Para cada estado de la empresa, añadirlos a una lista
        Anios.append(estado.idResultado.yearEstado)
    #Luego de obtener los años de los estados de la empresa, meterlos a un set para eliminar duplicados
    #y luego de eso devolverlos a una lista
    Anios = list(set(Anios))

    ##################OBTENER TODOS SALDOS DE LA EMPRESA##########################
    #Obtengo todos los saldos con los estados
    SaldosCuentasEmpresa = []
    #Para cada cuenta de la empresa
    for cuenta in Cuentas:
        if(cuenta.tipo_cuenta=="Estado de Resultado" or cuenta.tipo_cuenta=='6'):
            saldoCuentaAux = SaldoDeCuentaResultado.objects.filter(idCuenta=cuenta.idCuenta).first()
            if(saldoCuentaAux != None):
                #Añadir a Listado de saldo de cuentas, los saldos de cuentas correspondientes al listado de cuentas
                SaldosCuentasEmpresa.append(saldoCuentaAux)
        #Se tienen todos los saldos de cuentas de estados de resultado relacionados a las cuentas de la empresa

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
        #Contiene todas las cuentas de la empresa
        'salidaDebug1':Cuentas,
        #Contiene TODA la informacion de las cuentas de la empresa (saldos, anios, etc)
        'salidaDebug2':SaldosCuentasEmpresa,
        #Contiene la informacion general del estado especificado
        'resultadosAnio':Resultados,
        #Años que poseen estados de resultados
        'aniosConEstados':Anios,
        #Contiene la informacion ANUAL de las cuentas de la empresa (1 solo estado, el especificado)
        'saldosEstados':SaldoEstado,
        #Manda el id de la empresa a la template
        'empresa':EmpresaActual,
    }
    return render(request,'Estados/EstadoResultados.html', argumentos)