from django.shortcuts import render
from Empresa.models import Cuenta, SaldoDeCuentaResultado, SaldoDeCuentaBalace, EstadoEmpresa, BalanceEmpresa, Empresa
from Estados.models import EstadoDeResultado, Balance
from Estados.resources import EstadoResource
from tablib import Databook, Dataset
from django.contrib import messages
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from Estados.forms import EstadoForm
from Analisis.models import Analisis, LineaDeInforme

#Metodos para el sort()
def obtenerPorHorizontal(objeto):
    return objeto.porcentaje_horizontal

def obtenerPorVertical(objeto):
    return objeto.porcentaje_vertical

def indexEstados(request, empresa):
    ###################REQUEST POST######################
    #se ejecuta solo cuando la request es post
    if request.method == 'POST':
        #############POST CON ARCHIVO############## 
        #Obtendrá los saldos    
        if(len(request.FILES)!=0):
            ##Obtener variables para procesos##
            SaldoultimoResul = None
            try:
                #obtener del ultimo saldo de estadoresultado registrado en la base
                SaldoultimoResul = SaldoDeCuentaResultado.objects.latest('idSaldoResul')
            except SaldoDeCuentaResultado.DoesNotExist:
                SaldoultimoResul = None
            SaldoultimoBalance = None
            try:
                #obtener del ultimo saldo de balance general registrado en la base
                SaldoultimoBalance = SaldoDeCuentaBalace.objects.latest('idSaldo')
            except SaldoDeCuentaBalace.DoesNotExist:
                SaldoultimoBalance = None
            #Obtener todas las relaciones estado/empresa que corresponden a la empresa actual
            RelacionesEstadoEmpresa = EstadoEmpresa.objects.filter(idEmpresa=empresa)
            #Obtener todas las relaciones balance/empresa que corresponden a la empresa actual
            RelacionesBalanceEmpresa = BalanceEmpresa.objects.filter(idEmpresa=empresa)
            #Declara variable IdDelEstado como None (Para asegurar que será None en caso que falle proc)
            IdDelEstado = None
            #Declara variable IdDelBalance como None (Para asegurar que será None en caso que falle proc)
            IdDelBalance = None

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
            if(SaldoultimoResul != None):
                #obtener el id del ultimo saldo de estado ingresado
                idSaldoUltimoResul = SaldoultimoResul.idSaldoResul
            else:
                idSaldoUltimoResul = 0
            if(SaldoultimoBalance != None):
                #obtener el id del ultimo saldo de balance ingresado
                idSaldoUltimoBalance = SaldoultimoBalance.idSaldo
            else:
                idSaldoUltimoBalance = 0
            ActivoCorrienteMonto=[]
            PasivoCorrienteMonto=[]
            ActivoNoCorrienteMonto=[]
            PasivoNoCorrienteMonto=[]
            CapitalMonto=[]
            EstadosDeResultadosMonto=[]
            totalActivosCorriente = 0.0
            totalActivosNoCorriente = 0.0
            totalActivos = 0.0
            totalPasivosCorriente = 0.0
            totalPasivosNoCorriente = 0.0
            totalPasivos = 0.0
            totalCapital = 0.0
            ventasNetas = 0.0
            inventario=0.0
            inventarioAnterior=0.0
            activosCortoPlazo=0.0
            costoVentas=0.0
            cuentasPorCobrar=0.0
            cuentasPorCobraranterior=0.0
            cuentasPorPagar=0.0
            activoFijo=0.0
            costoOperacion=0.0
            gastoFinanciero=0.0
            otrosGastos=0.0
            otrosIngresos=0.0
            impuesto=0.0
            activoTotalAnterior=0.0
            anioAnalisis=None
            #ciclo con el archivo cargado en la instancia dataset
            #para cada registro en los datos importados
            cuentas=[]
            for registro in datosImportados:   
                try:
                    Cuenta.objects.get(idEmpresa=empresa,codigo_cuenta=registro[0])
                except:
                    return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje="Error:No existe una de las cuentas ingresadas, verifique su archivo.")
            for registro in datosImportados:   
                anioAnalisis=registro[2]
                #Se obtiene la cuenta con el id de la empresa y el codigo
                #(El codigo de la cuenta proviene de la primera columna del excel)
                cuentaObtenida = Cuenta.objects.get(idEmpresa=empresa,codigo_cuenta=registro[0])
                ################VERIFICAR TIPO DE CUENTA#####################
                #Reclasificar las cuentas por su tipo
                if(cuentaObtenida.idSobreNombre.sobreNombre=="Inventario"):
                    inventario = float(registro[3])
                    try:
                        inventarioAnteriorObj = SaldoDeCuentaBalace.objects.get(idCuenta=cuentaObtenida.idCuenta,year_saldo_Resul=datetime(registro[2]-1,1,1))
                        inventarioAnterior=float(inventarioAnteriorObj.monto_saldo)
                    except:
                        inventarioAnterior = 0
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Activo de corto plazo"):
                    activosCortoPlazo+=float(registro[3])
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Costo de servicio o ventas"):
                    costoVentas+=float(registro[3])
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Cuenta por cobrar"):
                    cuentasPorCobrar+=float(registro[3])
                    try:
                        cuentasPorCobraranteriorObj=SaldoDeCuentaBalace.objects.get(idCuenta=cuentaObtenida.idCuenta,year_saldo_Resul=datetime(registro[2]-1,1,1))
                        cuentasPorCobraranterior=float(cuentasPorCobraranteriorObj.monto_saldo)
                    except:
                        cuentasPorCobraranterior=0      
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Cuenta por pagar"):
                    cuentasPorPagar+=float(registro[3])
                    try:
                        cuentasPorPagaranteriorObj = SaldoDeCuentaBalace.objects.get(idCuenta=cuentaObtenida.idCuenta,year_saldo_Resul=datetime(registro[2]-1,1,1))
                        cuentasPorPagaranterior = float(cuentasPorPagaranteriorObj.monto_saldo)
                    except:
                        cuentasPorPagaranterior = 0                  
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Ventas netas"):
                    ventasNetas+=float(registro[3])
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Activo Fijo"):
                    activoFijo+=float(registro[3])
                    try:
                        activoFijoAnteriorObj = SaldoDeCuentaBalace.objects.get(idCuenta=cuentaObtenida.idCuenta,year_saldo_Resul=datetime(registro[2]-1,1,1))
                        activoFijoAnterior = float(activoFijoAnteriorObj.monto_saldo)
                    except:
                        activoFijoAnterior=0
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Costo de operación o administración"):
                    costoOperacion+=float(registro[3])
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Gastos financieros"):
                    gastoFinanciero+=float(registro[3])
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Otros gastos"):
                    otrosGastos+=float(registro[3])
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Otros ingresos"):
                    otrosIngresos+=float(registro[3])
                elif(cuentaObtenida.idSobreNombre.sobreNombre=="Impuestos"):
                    impuesto+=float(registro[3])
                
                if(cuentaObtenida.tipo_cuenta=="Estado de Resultado" or cuentaObtenida.tipo_cuenta=="6"):
                    #aumentar 1 al id
                    idSaldoUltimoResul += 1
                    #para cada estado de la empresa
                    for estadoempresa in RelacionesEstadoEmpresa:
                        #si el anio del estado actual corresponde a la tercera columna de los datos importados
                        #(La columna deben ser los años)
                        if(estadoempresa.idResultado.yearEstado==registro[2]):
                            #almacenar el id del estado
                            IdDelEstado = estadoempresa.idResultado
                    #Si al final del ciclo no se encuentra, levantar mensaje de error
                    #(Falta escribir un try-catch que capture la excepción y muestre mensaje de que no existe el estado)
                    try:
                        if(IdDelEstado==None):
                            raise TypeError("No existe el estado de resultado")
                    except:
                        return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje="Error:No existe el estado de resultado")
                    #instancia del modelo de SaldoDeCuentaResultado
                    valor = SaldoDeCuentaResultado(
                        #1. id
                        idSaldoResul=idSaldoUltimoResul,
                        #2. idcuenta
                        idCuenta=cuentaObtenida,
                        #3. idresultado
                        idResultado=IdDelEstado,
                        #4. año
                        year_saldo_Resul=datetime(registro[2],1,1),
                        #5. monto
                        monto_saldo_Resul=registro[3]
                    )
                    EstadosDeResultadosMonto.append(valor)
                    if(cuentaObtenida.idSobreNombre.sobreNombre=="Ventas netas"):
                        ventasNetas=valor.monto_saldo_Resul
                    #ejecutar insert
                    valor.save()
                elif(cuentaObtenida.tipo_cuenta=="Activo Corriente" or cuentaObtenida.tipo_cuenta=="1"):
                    #aumentar 1 al id
                    idSaldoUltimoBalance += 1
                    #para cada estado de la empresa
                    for balanceempresa in RelacionesBalanceEmpresa:
                        #si el anio del estado actual corresponde a la tercera columna de los datos importados
                        #(La columna deben ser los años)
                        if(balanceempresa.idbalance.yearEstado==registro[2]):
                            #almacenar el id del estado
                            IdDelBalance = balanceempresa.idbalance
                    #Si al final del ciclo no se encuentra, levantar mensaje de error
                    #(Falta escribir un try-catch que capture la excepción y muestre mensaje de que no existe el estado)
                    try:
                        if(IdDelBalance==None):
                            raise TypeError("No existe el balance general")
                    except:
                        return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje="Error:No existe el balance general")
                    #instancia del modelo de SaldoDeCuentaResultado
                    valor = SaldoDeCuentaBalace(
                        #1. id
                        idSaldoUltimoBalance,
                        #2. idcuenta
                        cuentaObtenida.idCuenta,
                        #3. idresultado
                        IdDelBalance.idBalance,
                        #4. año
                        datetime(registro[2],1,1),
                        #5. monto
                        registro[3]
                    )
                    #ejecutar insert
                    valor.save()
                    saldoAnterior = SaldoDeCuentaBalace.objects.get(idCuenta=cuentaObtenida.idCuenta,year_saldo_Resul=datetime(registro[2]-1,1,1))
                    activoTotalAnterior += saldoAnterior.monto_saldo
                    #anexar ese saldo a una lista de saldos de activos corrientes
                    ActivoCorrienteMonto.append(valor)
                    #sumar el saldo
                    totalActivosCorriente += valor.monto_saldo
                elif(cuentaObtenida.tipo_cuenta=="Activo no Corriente" or cuentaObtenida.tipo_cuenta=="2"):
                    #aumentar 1 al id
                    idSaldoUltimoBalance += 1
                    #para cada estado de la empresa
                    for balanceempresa in RelacionesBalanceEmpresa:
                        #si el anio del estado actual corresponde a la tercera columna de los datos importados
                        #(La columna deben ser los años)
                        if(balanceempresa.idbalance.yearEstado==registro[2]):
                            #almacenar el id del estado
                            IdDelBalance = balanceempresa.idbalance
                    #Si al final del ciclo no se encuentra, levantar mensaje de error
                    #(Falta escribir un try-catch que capture la excepción y muestre mensaje de que no existe el estado)
                    try:
                        if(IdDelBalance==None):
                            raise TypeError("No existe el balance general")
                    except:
                        return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje="Error:No existe el balance general")
                    #instancia del modelo de SaldoDeCuentaResultado
                    valor = SaldoDeCuentaBalace(
                        #1. id
                        idSaldoUltimoBalance,
                        #2. idcuenta
                        cuentaObtenida.idCuenta,
                        #3. idresultado
                        IdDelBalance.idBalance,
                        #4. año
                        datetime(registro[2],1,1),
                        #5. monto
                        registro[3]
                    )
                    #ejecutar insert
                    valor.save()
                    saldoAnterior = SaldoDeCuentaBalace.objects.get(idCuenta=cuentaObtenida.idCuenta,year_saldo_Resul=datetime(registro[2]-1,1,1))
                    activoTotalAnterior += saldoAnterior.monto_saldo
                    ActivoNoCorrienteMonto.append(valor)
                    totalActivosNoCorriente+=valor.monto_saldo
                elif(cuentaObtenida.tipo_cuenta=="Pasivo Corriente" or cuentaObtenida.tipo_cuenta=="3"):
                    #aumentar 1 al id
                    idSaldoUltimoBalance += 1
                    #para cada estado de la empresa
                    for balanceempresa in RelacionesBalanceEmpresa:
                        #si el anio del estado actual corresponde a la tercera columna de los datos importados
                        #(La columna deben ser los años)
                        if(balanceempresa.idbalance.yearEstado==registro[2]):
                            #almacenar el id del estado
                            IdDelBalance = balanceempresa.idbalance
                    #Si al final del ciclo no se encuentra, levantar mensaje de error
                    #(Falta escribir un try-catch que capture la excepción y muestre mensaje de que no existe el estado)
                    try:
                        if(IdDelBalance==None):
                            raise TypeError("No existe el balance general")
                    except:
                        return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje="Error:No existe el balance general")
                    #instancia del modelo de SaldoDeCuentaResultado
                    valor = SaldoDeCuentaBalace(
                        #1. id
                        idSaldoUltimoBalance,
                        #2. idcuenta
                        cuentaObtenida.idCuenta,
                        #3. idresultado
                        IdDelBalance.idBalance,
                        #4. año
                        datetime(registro[2],1,1),
                        #5. monto
                        registro[3]
                    )
                    #ejecutar insert
                    valor.save()
                    PasivoCorrienteMonto.append(valor)
                    totalPasivosCorriente+=valor.monto_saldo
                elif(cuentaObtenida.tipo_cuenta=="Pasivo no Corriente" or cuentaObtenida.tipo_cuenta=="4"):
                    #aumentar 1 al id
                    idSaldoUltimoBalance += 1
                    #para cada estado de la empresa
                    for balanceempresa in RelacionesBalanceEmpresa:
                        #si el anio del estado actual corresponde a la tercera columna de los datos importados
                        #(La columna deben ser los años)
                        if(balanceempresa.idbalance.yearEstado==registro[2]):
                            #almacenar el id del estado
                            IdDelBalance = balanceempresa.idbalance
                    #Si al final del ciclo no se encuentra, levantar mensaje de error
                    #(Falta escribir un try-catch que capture la excepción y muestre mensaje de que no existe el estado)
                    try:
                        if(IdDelBalance==None):
                            raise TypeError("No existe el balance general")
                    except:
                        return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje="Error:No existe el balance general")
                    #instancia del modelo de SaldoDeCuentaResultado
                    valor = SaldoDeCuentaBalace(
                        #1. id
                        idSaldoUltimoBalance,
                        #2. idcuenta
                        cuentaObtenida.idCuenta,
                        #3. idresultado
                        IdDelBalance.idBalance,
                        #4. año
                        datetime(registro[2],1,1),
                        #5. monto
                        registro[3]
                    )
                    #ejecutar insert
                    valor.save()
                    PasivoNoCorrienteMonto.append(valor)
                    totalPasivosNoCorriente+=valor.monto_saldo
                elif(cuentaObtenida.tipo_cuenta=="Capital" or cuentaObtenida.tipo_cuenta=="5"):
                    #aumentar 1 al id
                    idSaldoUltimoBalance += 1
                    #para cada estado de la empresa
                    for balanceempresa in RelacionesBalanceEmpresa:
                        #si el anio del estado actual corresponde a la tercera columna de los datos importados
                        #(La columna deben ser los años)
                        if(balanceempresa.idbalance.yearEstado==registro[2]):
                            #almacenar el id del estado
                            IdDelBalance = balanceempresa.idbalance
                    #Si al final del ciclo no se encuentra, levantar mensaje de error
                    #(Falta escribir un try-catch que capture la excepción y muestre mensaje de que no existe el estado)
                    try:
                        if(IdDelBalance==None):
                            raise TypeError("No existe el balance general")
                    except:
                        return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje="Error:No existe el balance general")
                    #instancia del modelo de SaldoDeCuentaResultado
                    valor = SaldoDeCuentaBalace(
                        #1. id
                        idSaldoUltimoBalance,
                        #2. idcuenta
                        cuentaObtenida.idCuenta,
                        #3. idresultado
                        IdDelBalance.idBalance,
                        #4. año
                        datetime(registro[2],1,1),
                        #5. monto
                        registro[3]
                    )
                    #ejecutar insert
                    valor.save()
                    CapitalMonto.append(valor)
                    totalCapital+=valor.monto_saldo
            totalActivos = totalActivosCorriente + totalActivosNoCorriente
            totalPasivos = totalPasivosCorriente + totalPasivosNoCorriente
            ###########PROCESO ANALISIS###############
            if(anioAnalisis==None):
                    UltimoBalance = BalanceEmpresa.objects.filter(idEmpresa=empresa).latest('idbalance')
                    anioAnalisis=UltimoBalance.idbalance.yearEstado

            #####OBTENER EL BALANCE ACTUAL Y EL ANTERIOR
            balanceAnalisis = None
            balanceAnterior = None
            #Obtiene todas las relaciones balance/empresa
            BalancesEmpresa = BalanceEmpresa.objects.filter(idEmpresa=empresa).order_by('idbalance')
            #Para cada relacion balance-empresa
            for balance in BalancesEmpresa:
                #Si el año del balance de la relación es igual al 
                if(balance.idbalance.yearEstado == anioAnalisis):
                    balanceAnalisis = balance.idbalance
                if(balance.idbalance.yearEstado == (anioAnalisis-1)):
                    balanceAnterior = balance.idbalance
            #####OBTENER EL ESTADO ACTUAL Y EL ANTERIOR
            estadoAnalisis = None
            estadoAnterior = None
            #Obtiene todas las relaciones estado resultado/empresa
            ResultadosEmpresa = EstadoEmpresa.objects.filter(idEmpresa=empresa).order_by('idResultado')
            for resultadoEmpresa in ResultadosEmpresa:
                if(resultadoEmpresa.idResultado.yearEstado == anioAnalisis):
                    estadoAnalisis = resultadoEmpresa.idResultado
                if(resultadoEmpresa.idResultado.yearEstado == (anioAnalisis -1 )):
                    estadoAnterior = resultadoEmpresa.idResultado
            #####SI AMBOS EXISTEN
            if(balanceAnterior != None and estadoAnterior != None):
                #####CREAR OBJETO NUEVO ANALISIS
                UltimoAnalisis = None
                #Inicializa variables de id a cero
                IdUltimoAnalisis = 0
                try:
                    #Obtener el último Balance ingresado
                    UltimoAnalisis = Analisis.objects.latest('idAnalisis')
                #Si no existe
                except Analisis.DoesNotExist:
                    #Asegurarse que sea None
                    UltimoAnalisis = None
                ####ID ANALISIS
                #si es None
                if(UltimoAnalisis==None):
                    #El id será 1
                    IdUltimoAnalisis = 1
                else:
                    #Caso contrario, tomar el último id y sumar 1
                    IdUltimoAnalisis = UltimoAnalisis.idAnalisis + 1
                #Crea objeto análisis
                anali = Analisis(
                    idAnalisis = IdUltimoAnalisis,
                    idEmpresa= Empresa.objects.get(idEmpresa=empresa),
                    year_analisis = anioAnalisis,
                    year_previos = anioAnalisis - 1,
                    conclusion_horizontal = "",
                    conclusion_vertical = "",
                )
                anali.save()
                anali.estadosParaAnalisis.add(estadoAnalisis)
                anali.estadosParaAnalisis.add(estadoAnterior)
                anali.balancesParaAnalisis.add(balanceAnalisis)
                anali.balancesParaAnalisis.add(balanceAnterior)
                ###########Obtener cuentas para el proceso#########
                montosActivo = ActivoCorrienteMonto + ActivoNoCorrienteMonto
                montosPasivoCapital = PasivoCorrienteMonto + PasivoNoCorrienteMonto + CapitalMonto
                cuentasBalanceAnalisisAnt = SaldoDeCuentaBalace.objects.filter(idbalance=balanceAnterior)
                cuentasEstadoAnalisisAnt = SaldoDeCuentaResultado.objects.filter(idResultado=estadoAnterior)
                ###########Realizar analisis horizontal y vertical
                LineasActivos = []
                LineasPasivos = []
                LineasCapital = []
                LineasEstados = []
                for cuentaActual in montosActivo:
                    for cuentaAnterior in cuentasBalanceAnalisisAnt:
                        variacionHorizontal = 0.0
                        porcentajeHorizontal = 0.0
                        if(cuentaActual.idCuenta == cuentaAnterior.idCuenta):
                            porcentajeHorizontal = cuentaActual.monto_saldo/float(cuentaAnterior.monto_saldo) - 1
                            variacionHorizontal = cuentaActual.monto_saldo - float(cuentaAnterior.monto_saldo)
                            porcentajeVertical = cuentaActual.monto_saldo / totalActivos
                            linea=LineaDeInforme(
                                idCuenta=cuentaActual.idCuenta,
                                idAnalisis=anali,
                                variacion_horizontal = variacionHorizontal,
                                porcentaje_horizontal = porcentajeHorizontal,
                                porcentaje_vertical = porcentajeVertical,
                            )
                            LineasActivos.append(linea)
                            linea.save()
                for cuentaActual in montosPasivoCapital:
                    for cuentaAnterior in cuentasBalanceAnalisisAnt:
                        variacionHorizontal = 0.0
                        porcentajeHorizontal = 0.0
                        porcentajeVertical = 0.0
                        if(cuentaActual.idCuenta == cuentaAnterior.idCuenta):
                            porcentajeHorizontal = cuentaActual.monto_saldo/float(cuentaAnterior.monto_saldo) - 1
                            variacionHorizontal = cuentaActual.monto_saldo - float(cuentaAnterior.monto_saldo)
                            porcentajeVertical = cuentaActual.monto_saldo / (totalPasivos + totalCapital)
                            linea=LineaDeInforme(
                                idCuenta=cuentaActual.idCuenta,
                                idAnalisis=anali,
                                variacion_horizontal = variacionHorizontal,
                                porcentaje_horizontal = porcentajeHorizontal,
                                porcentaje_vertical = porcentajeVertical,
                            )
                            if(cuentaActual.idCuenta.tipo_cuenta == "Capital"):
                                LineasCapital.append(linea)
                            else:
                                LineasPasivos.append(linea)
                            linea.save()
                for cuentaActual in EstadosDeResultadosMonto:
                    for cuentaAnterior in cuentasEstadoAnalisisAnt:
                        variacionHorizontal = 0.0
                        porcentajeHorizontal = 0.0
                        porcentajeVertical = 0.0
                        if(cuentaActual.idCuenta == cuentaAnterior.idCuenta and ventasNetas!=0.0):
                            porcentajeHorizontal = cuentaActual.monto_saldo_Resul/float(cuentaAnterior.monto_saldo_Resul) - 1
                            variacionHorizontal = cuentaActual.monto_saldo_Resul - float(cuentaAnterior.monto_saldo_Resul)
                            porcentajeVertical = cuentaActual.monto_saldo_Resul / ventasNetas
                            linea=LineaDeInforme(
                                idCuenta=cuentaActual.idCuenta,
                                idAnalisis=anali,
                                variacion_horizontal = variacionHorizontal,
                                porcentaje_horizontal = porcentajeHorizontal,
                                porcentaje_vertical = porcentajeVertical,
                            )
                            LineasEstados.append(linea)
                            linea.save()
                activosOrdenadosVertical = sorted(LineasActivos,key=obtenerPorVertical)
                pasivosOrdenadosVertical = sorted(LineasPasivos,key=obtenerPorVertical)
                capitalOrdenadosVertical = sorted(LineasCapital,key=obtenerPorVertical)
                estadoOrdenadosVertical = sorted(LineasEstados,key=obtenerPorVertical)
                mayorVariacionActivoVertical = activosOrdenadosVertical[0].idCuenta.nombre_cuenta
                menorVariacionActivoVertical = activosOrdenadosVertical[len(activosOrdenadosVertical)-1:][0].idCuenta.nombre_cuenta
                cadenaVertical = "Se recomienda prestar atención a la cuenta " + mayorVariacionActivoVertical + " dado que presenta la mayor parte de los activos de la empresa. "
                cadenaVertical+= "Lo que quiere decir que la mayor parte de la inversión se encuentra en el " + activosOrdenadosVertical[0].idCuenta.tipo_cuenta + " de la empresa."
                if(activosOrdenadosVertical[len(activosOrdenadosVertical)-1:][0].porcentaje_vertical > 0):
                    cadenaVertical +=  "Por otro lado, la cuenta "+ menorVariacionActivoVertical + " ha presentado la menor variación entre los activos."
                elif(activosOrdenadosVertical[len(activosOrdenadosVertical)-1:][0].porcentaje_vertical == 0):
                    cadenaVertical +=  "Por otro lado, la cuenta "+ menorVariacionActivoVertical + " no ha presentado variación en lo absoluto."
                else:
                    cadenaVertical +=  "Por otro lado, la cuenta "+ menorVariacionActivoVertical + " ha presentado una reducción entre los activos de la empresa."
                mayorVariacionPasivoVertical = pasivosOrdenadosVertical[0].idCuenta.nombre_cuenta
                cadenaVertical += "La inversión de la empresa se financia con un " + str(pasivosOrdenadosVertical[0].porcentaje_vertical*100) + str(chr(37)) +" de inversiones de terceros, representado en " + mayorVariacionPasivoVertical + " de la empresa, "
                cadenaVertical += "y con un " + str(capitalOrdenadosVertical[0].porcentaje_vertical*100) + str(chr(37)) +" de inversiones propias, representado en " + mayorVariacionPasivoVertical + ". "
                cadenaVertical += "La mayor reducción de utilidad proviene del " + estadoOrdenadosVertical[0].idCuenta.nombre_cuenta + " de la empresa, representando un " + str(estadoOrdenadosVertical[0].porcentaje_vertical*100) + str(chr(37)) + "del ingreso por ventas."
                anali.conclusion_vertical = cadenaVertical
                activosOrdenadosHorizontal = sorted(LineasActivos,key=obtenerPorHorizontal)
                pasivosOrdenadosHorizontal = sorted(LineasPasivos,key=obtenerPorHorizontal)
                captialOrdenadosHorizontal = sorted(LineasCapital,key=obtenerPorHorizontal)
                estadoOrdenadosHorizontal = sorted(LineasEstados,key=obtenerPorHorizontal)
                mayorVariacionActivoHorizontal = activosOrdenadosHorizontal[0].idCuenta.nombre_cuenta
                mayorPorcentajeActivoHorizontal = activosOrdenadosHorizontal[0].porcentaje_vertical*100
                mayorVariacionPasivoHorizontal = pasivosOrdenadosHorizontal[0].idCuenta.nombre_cuenta
                mayorPorcentajePasivoHorizontal = pasivosOrdenadosHorizontal[0].porcentaje_vertical*100
                mayorVariacionCapitalHorizontal = captialOrdenadosHorizontal[0].idCuenta.nombre_cuenta
                mayorPorcentajeCapitalHorizontal = captialOrdenadosHorizontal[0].porcentaje_vertical*100
                mayorVariacionEstadoHorizontal= estadoOrdenadosHorizontal[0].idCuenta.nombre_cuenta
                mayorPorcentajeEstadoHorizontal = estadoOrdenadosHorizontal[0].porcentaje_vertical*100
                cadenaHorizontal = "La mayor variación con respecto al año pasado, se presenta en los " + activosOrdenadosHorizontal[0].idCuenta.tipo_cuenta + " siendo la cuenta " + mayorVariacionActivoHorizontal + " la que presenta la mayor variación con un " + str(mayorPorcentajeActivoHorizontal) + str(chr(37)) + ". "
                cadenaHorizontal += "Por otro lado la mayor variación de la empresa se presentó en " + mayorVariacionCapitalHorizontal + " con una variación del " + str(mayorPorcentajeCapitalHorizontal) + str(chr(37)) + ". "
                cadenaHorizontal += "Mientras que, las inversiones de terceros tuvieron su mayor variación en " + mayorVariacionPasivoHorizontal + " con un " + str(mayorPorcentajePasivoHorizontal) + str(chr(37)) + " con respecto al año pasado. "
                if(estadoOrdenadosHorizontal[0].idCuenta.naturaleza_cuenta=="Acreedor"):
                    cadenaHorizontal += "En el estado de resultados, se destaca el aumento en los ingresos de la empresa."
                else:
                    cadenaHorizontal+="Es importante prestar especial atención a los gastos de la empresa, puesto que han presentado una variación importante con respecto al año pasado."
                anali.conclusion_horizontal = cadenaHorizontal
                anali.save()
                razonLiquidezCorriente = totalActivosCorriente / totalPasivosCorriente
                razonLiquidezRapida = (totalActivosCorriente  - inventario) / totalPasivosCorriente 
                razonCapitalTrabajo = (totalActivosCorriente - totalPasivosCorriente) / totalActivos
                razonEfectivo = (activosCortoPlazo + cuentasPorCobrar) / totalPasivosCorriente
                promedioInventario = (inventario+inventarioAnterior)/2
                razonRotacionInventario = costoVentas / promedioInventario
                diasInventario = promedioInventario / (costoVentas/365)
                promedioCuentasPorCobrar = (cuentasPorCobrar + cuentasPorCobraranterior) / 2
                razonRotacionCobros = ventasNetas / promedioCuentasPorCobrar
                periodoMedioCobranza =promedioCuentasPorCobrar * 365 / ventasNetas
                promedioCuentasPorPagar = (cuentasPorPagar + cuentasPorPagaranterior) / 2
                razonRotacionPagos = (costoVentas - inventario) / promedioCuentasPorPagar
                periodoMedioPagos = promedioCuentasPorPagar * 365 / (costoVentas - inventario)
                promedioActivoTotal = (activoTotalAnterior + totalActivos) / 2
                razonRotacionActivosTotales = ventasNetas / promedioActivoTotal
                promedioActivoFijo = (activoFijo + activoFijoAnterior) / 2
                razonRotacionActivosFijos = ventasNetas/promedioActivoFijo
                utilidadBruta = ventasNetas - costoVentas
                utilidadOperativa = utilidadBruta - costoOperacion - gastoFinanciero
                utilidadAntesImpuesto = utilidadOperativa + otrosIngresos - otrosGastos
                utilidadNeta = utilidadAntesImpuesto - impuesto
                indiceMargenBruto = utilidadBruta / ventasNetas
                indiceMargenOperativo = utilidadOperativa /ventasNetas
                gradoEndeudamiento = totalPasivos / totalActivos
                gradoPropiedad = totalCapital / totalActivos
                endeudamientoPatrimonial = totalPasivos / totalCapital
                coberturaGastosFinancieros = utilidadAntesImpuesto / gastoFinanciero
                return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje="Se agregaron los saldos correctamente.")
        ###############POST SIN ARCHIVOS################
        #para request post sin archivos, obtendrá el form
        else:
            #Usando la request POST, crear un formulario de tipo EstadoForm
            formulario=EstadoForm(request.POST)
            #Si el form POSTeado es válido (pendiente de modificar is_valid)
            if(formulario.is_valid()):
                empresaActual = Empresa.objects.get(idEmpresa=empresa)
                #Obtiene todos los balances de la empresa
                BalancesEmpresa = BalanceEmpresa.objects.filter(idEmpresa=empresa).order_by('idbalance')
                #Luz verde para empezar a insertar
                LuzVerde = True
                #Para cada estado de la empresa
                for balance in BalancesEmpresa:
                    #Si el estado es del año dado
                    if(str(balance.idbalance.yearEstado)==str(formulario.data.get("yearEstado"))):
                        #Negar el continuar con el proceso
                        LuzVerde = False
                if(LuzVerde==True):
                    #####PROCESO PARA INSERTAR NUEVO BALANCE
                    #Declara variables como None
                    UltimoBalance = None
                    UltimoEstado = None
                    #Inicializa variables de id a cero
                    IdBalanceUltimo = 0
                    IdUltimoEstado = 0
                    #Inicializa el nombre de la moneda a ""
                    NombreMoneda = ""
                    try:
                        #Obtener el último Balance ingresado
                        UltimoBalance = Balance.objects.latest('idBalance')
                    #Si no existe
                    except Balance.DoesNotExist:
                        #Asegurarse que sea None
                        UltimoBalance = None
                    #Si el último balance no existe
                    if(UltimoBalance==None):
                        #Definir el Id como 1
                        IdBalanceUltimo = 1
                    else:
                        #Caso contrario, tomar el id del último balance y sumar 1
                        IdBalanceUltimo = UltimoBalance.idBalance + 1
                    try:
                        #Obtener el último estado de resultado
                        UltimoEstado = EstadoDeResultado.objects.latest('idResultado')
                    #Si no existe
                    except EstadoDeResultado.DoesNotExist:
                        #Asegurarse que sea None
                        UltimoEstado = None
                    #si es None
                    if(UltimoEstado==None):
                        #El id será 1
                        IdUltimoEstado = 1
                    else:
                        #Caso contrario, tomar el último id y sumar 1
                        IdUltimoEstado = UltimoEstado.idResultado + 1
                    #Obtener el código de la moneda del campo del formulario
                    CodigoMoneda = formulario.data.get("moneda_codigo_balance")
                    #Obtener las opciones del select de monedas del formulario
                    dictMonedasOpciones = formulario.fields.get("moneda_codigo_balance").choices
                    #Para cada opción
                    for moneda in dictMonedasOpciones:
                        #Si la moneda corresponde al código obtenido del formulario
                        if(moneda[0]==CodigoMoneda):
                            #Almacenar el nombre
                            NombreMoneda=moneda[1]
                    #Crear instancia Balance
                    instanciaBalance = Balance(
                        #Id del balance
                        idBalance=IdBalanceUltimo,
                        #fecha de inicio del formulario
                        fechaInicioBalance=formulario.data.get("fechaInicioBalance"),
                        #fecha de fin del formulario
                        fechaFinBalance=formulario.data.get("fechaFinBalance"),
                        #año
                        yearEstado=formulario.data.get("yearEstado"),
                        #nombre
                        moneda_balance=NombreMoneda,
                        #codigo
                        moneda_codigo_balance=CodigoMoneda,
                    )
                    #insertar registro
                    instanciaBalance.save()
                    #Crear instancia estado resultado
                    instanciaResultado = EstadoDeResultado(
                        idResultado=IdUltimoEstado,
                        fechaInicioEstado=formulario.data.get("fechaInicioBalance"),
                        fechaFinEstado=formulario.data.get("fechaFinBalance"),
                        yearEstado=formulario.data.get("yearEstado"),
                        moneda_estado=NombreMoneda,
                        moneda_codigo_estado=CodigoMoneda,
                    )
                    #insertar registro
                    instanciaResultado.save()
                    instanciaRelacionBalance = BalanceEmpresa(
                        idbalance=Balance.objects.get(idBalance=IdBalanceUltimo),
                        idEmpresa=empresaActual
                    )
                    instanciaRelacionEstado = EstadoEmpresa(
                        idResultado=EstadoDeResultado.objects.get(idResultado=IdUltimoEstado),
                        idEmpresa=empresaActual
                    )
                    instanciaRelacionBalance.save()
                    instanciaRelacionEstado.save()
                    exito="Se inserto con exito el estado financiero."
                    return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje=exito)
                else:
                    exito="No se inserto ha podido insertar el estado, ya existe."
                    return redirect('Estados:redireccionConfirmacion',empresa=empresa,mensaje=exito)
        #para ambos posts
        argumentos = {}
    #############REQUEST GET#################33
    #Para request get
    else:
        empresaActual = Empresa.objects.get(idEmpresa=empresa)
        argumentos = {
            "idEmpresaActual":empresa,
            "ListaBalances":empresaActual.BalancesDeEmpresa.all(),
            "formIngresarEstado":EstadoForm()
        }
    return render(request, 'Estados/EstadosIndex.html',argumentos)

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
    Anios.sort()

    ##################OBTENER TODOS SALDOS DE LA EMPRESA##########################
    #Obtengo todos los saldos con los estados
    SaldosCuentasEmpresa = []
    #Para cada cuenta de la empresa
    for cuenta in Cuentas:
        if(cuenta.tipo_cuenta=="Estado de Resultado" or cuenta.tipo_cuenta=='6'):
            saldoCuentaAux = SaldoDeCuentaResultado.objects.filter(idCuenta=cuenta.idCuenta)
            if(saldoCuentaAux != None):
                for saldoAuxiliar in saldoCuentaAux:
                    #Añadir a Listado de saldo de cuentas, los saldos de cuentas correspondientes al listado de cuentas
                    SaldosCuentasEmpresa.append(saldoAuxiliar)
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

# Index de balance general
def indexBalanceGeneral(request, empresa, anio):
    ##################OBTENER TODAS LAS CUENTAS DE LA EMPRESA##########################
    #Obtengo todas las cuentas de la empresa
    Cuentas = Cuenta.objects.filter(idEmpresa=empresa).order_by('idCuenta')
    
    ##################OBTENER LA EMPRESA#############################
    EmpresaActual = Empresa.objects.get(idEmpresa=empresa)

    ##################OBTENER TODOS LOS ESTADOS DE LA EMPRESA##########################
    #Obtengo todos los estados de resultado de la empresa (tengo los idResultado)
    BalancesEmpresa = BalanceEmpresa.objects.filter(idEmpresa=empresa).order_by('idbalance')

    #Obtengo el estado del anio dado    
    Balances = []
    Anios = []
    #Para cada estado de la empresa
    for balance in BalancesEmpresa:
        #Si el estado es del año dado
        if(balance.idbalance.yearEstado==anio):
            #Añadir a Estados de Resultados del año
            Balances.append(balance.idbalance)
        #Para cada estado de la empresa, añadirlos a una lista
        Anios.append(balance.idbalance.yearEstado)
    #Luego de obtener los años de los estados de la empresa, meterlos a un set para eliminar duplicados
    #y luego de eso devolverlos a una lista
    Anios = list(set(Anios))
    Anios.sort()

    ##################OBTENER TODOS SALDOS DE LA EMPRESA##########################
    #Obtengo todos los saldos con los estados
    SaldosCuentasEmpresa = []
    #Para cada cuenta de la empresa
    for cuenta in Cuentas:
        #Si la cuenta NO es de Estado de resultado
        if(cuenta.tipo_cuenta!="Estado de Resultado" or cuenta.tipo_cuenta!='6'):
            #El saldo de cuenta que se almacenará sera
            #el primer saldo de cuenta que coincide con el id de la cuenta actual
            saldoCuentaAux = SaldoDeCuentaBalace.objects.filter(idCuenta=cuenta.idCuenta)
            if(saldoCuentaAux != None):
                for saldoAuxiliar in saldoCuentaAux:
                    #Añadir a Listado de saldo de cuentas, los saldos de cuentas correspondientes al listado de cuentas
                    SaldosCuentasEmpresa.append(saldoAuxiliar)
        #Se tienen todos los saldos de cuentas de estados de resultado relacionados a las cuentas de la empresa

    #Obtengo los saldos del estado de resultado
    SaldosDelBalance = []
    if(len(Balances)>0):
        BalanceActual = Balances[0]
        #Para cada saldo de las cuentas de la empresa
        for saldoEmpresa in SaldosCuentasEmpresa:
            if(saldoEmpresa.year_saldo.year == BalanceActual.yearEstado):
                #Añadir a los Saldos del estado de resultado del mismo anio
                SaldosDelBalance.append(saldoEmpresa)

    argumentos = {
        #Contiene todas las cuentas de la empresa
        'salidaDebug1':Cuentas,
        #Contiene TODA la informacion de las cuentas de la empresa (saldos, anios, etc)
        'salidaDebug2':SaldosCuentasEmpresa,
        #Contiene la informacion general del estado especificado
        'balancesAnio':Balances,
        #Años que poseen estados de resultados
        'aniosConEstados':Anios,
        #Contiene la informacion ANUAL de las cuentas de la empresa (1 solo estado, el especificado)
        'saldosBalance':SaldosDelBalance,
        #Manda el id de la empresa a la template
        'empresa':EmpresaActual,
    }
    return render(request,'Estados/BalanceGeneral.html', argumentos)

def mensajeRedireccion(request,mensaje,empresa):
    return render(request,'Estados/mensajeRedireccion.html', {'mensaje':mensaje,'empresa':empresa})