from django.shortcuts import render
from Empresa.models import Cuenta, SaldoDeCuentaResultado, SaldoDeCuentaBalace, EstadoEmpresa, BalanceEmpresa, Empresa
from Estados.models import EstadoDeResultado, Balance
from Estados.resources import EstadoResource
from tablib import Databook, Dataset
from django.contrib import messages
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect
from Estados.forms import EstadoForm
from Analisis.models import Analisis, LineaDeInforme, RatiosAnalisis
from Giro.models import Ratios, Giro, DatoGiro
from Usuarios.models import AccesoUsuario, User
from django.http import Http404, HttpResponse
from django.core import exceptions
from decimal import *
from Estados.forms import SaldoCuentaForm

#Metodos para el sort()
def obtenerPorHorizontal(objeto):
    return objeto.porcentaje_horizontal

def obtenerPorVertical(objeto):
    return objeto.porcentaje_vertical

def mostrarMensajeSegunRol(request,mensajeR,idemp=None):
    idRolUsuarioActual=request.user.rol
    if(idRolUsuarioActual==3):
        return redirect('Estados:redireccionConfirmacion',mensaje=mensajeR)
    else:
        return redirect('Estados:redireccionConfirmacion',mensaje=mensajeR, empresaidmen=idemp)
#usage: return mostrarMensajeSegunRol(request, reemplazarmensajeaqui, idempresadmin)

def indexEstados(request,idempresadmin=None):
    #de codigo del form para los accesos
    op = '005'
    #obtiene el usuario de la sesión actual
    idUsuarioActual = request.user.id
    idRolUsuarioActual = request.user.rol
    #obtiene la tupla de acceso del usuario actual al form actual
    usac=AccesoUsuario.objects.filter(idUsuario=idUsuarioActual,idOpcion=op).first()
    esGerente=False
    #Si el acceso existe
    if(usac!=None):
        if(idRolUsuarioActual==3):
            empresaActual=get_object_or_404(Empresa,gerente=idUsuarioActual)
            esGerente= True
        else:
            empresaActual=Empresa.objects.filter(idEmpresa=idempresadmin).first()
            esGerente = False
            if(empresaActual==None):
                 raise Http404("Oops, esta página no existe.")
        empresa = empresaActual.idEmpresa
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
                    return mostrarMensajeSegunRol(request, "Error: El formato del archivo no es el correcto. Por favor, asegurese que ha subido un archivo con extensión .xlsx", idempresadmin)
                #crear instancia tablib Dataset
                conjuntoDatos = Dataset()
                #Definir headers del dataset
                #Estos son los headers que debe tener la tabla de excel
                conjuntoDatos.headers = ('Codigo de Cuenta', 'Nombre de la cuenta', 'Anio del Estado', 'Monto')
                #cargar el archivo de la request en la instancia Dataset
                datosImportados = conjuntoDatos.load(archivo.read(),format='xlsx')
                if(SaldoultimoResul != None):
                    #obtener el id del ultimo saldo de estado ingresado
                    idSaldoUltimoResul =  SaldoultimoResul.idSaldoResul
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
                        cuentaRegistro = Cuenta.objects.get(idEmpresa=empresa,codigo_cuenta=registro[0])
                    except Cuenta.DoesNotExist:
                        return mostrarMensajeSegunRol(request, "Error:No existe una de las cuentas ingresadas, verifique su archivo.", idempresadmin)
                    except Cuenta.MultipleObjectsReturned:
                        return mostrarMensajeSegunRol(request, "Error:Código de cuentas repetido, revise su catálogo e intente nuevamente.", idempresadmin)
                    anioIntentaIngresar = SaldoDeCuentaBalace.objects.filter(year_saldo=datetime(registro[2],1,1))
                    for saldo in anioIntentaIngresar:
                        if saldo.idCuenta.idEmpresa.idEmpresa==empresa:
                            saldo.delete()
                    anioIntentaIngresarResul = SaldoDeCuentaResultado.objects.filter(year_saldo_Resul=datetime(registro[2],1,1))
                    for saldoRes in anioIntentaIngresarResul:
                        if saldoRes.idCuenta.idEmpresa.idEmpresa==empresa:
                            saldoRes.delete()
                            #if(len(listaAux)!=0):
                        #return mostrarMensajeSegunRol(request, "Error:Ya ha añadido saldos para este estado.", idempresadmin)
                for registro in datosImportados:   
                    anioAnalisis=registro[2]
                    #Se obtiene la cuenta con el id de la empresa y el codigo
                    #(El codigo de la cuenta proviene de la primera columna del excel)
                    cuentaObtenida = Cuenta.objects.get(idEmpresa=empresa,codigo_cuenta=registro[0])
                    ################VERIFICAR TIPO DE CUENTA#####################
                    #Reclasificar las cuentas por su tipo
                    cuentasPorPagaranterior = 0
                    activoFijoAnterior=0
                    razonRotacionInventario=0
                    diasInventario=0
                    razonRotacionCobros=0
                    periodoMedioCobranza=0
                    razonRotacionPagos=0
                    periodoMedioPagos=0
                    razonRotacionActivosFijos=0
                    indiceMargenBruto=0
                    indiceMargenOperativo=0
                    coberturaGastosFinancieros=0
                    if(cuentaObtenida.idSobreNombre!=None):
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
                    
                    if(cuentaObtenida.tipo_cuenta=="Estado de Resultado" or cuentaObtenida.tipo_cuenta=="Estado\xa0de\xa0Resultado"):
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
                            return mostrarMensajeSegunRol(request, "Error:No existe el estado de resultado", idempresadmin)
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
                        if(cuentaObtenida.idSobreNombre!=None):
                            if(cuentaObtenida.idSobreNombre.sobreNombre=="Ventas netas"):
                                ventasNetas=valor.monto_saldo_Resul
                        #ejecutar insert
                        valor.save()
                    elif(cuentaObtenida.tipo_cuenta=="Activo Corriente" or cuentaObtenida.tipo_cuenta=="Activo\xa0Corriente"):
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
                            return mostrarMensajeSegunRol(request, "Error:No existe el balance general", idempresadmin)
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
                        saldoAnterior = SaldoDeCuentaBalace.objects.filter(idCuenta=cuentaObtenida.idCuenta,year_saldo=datetime(registro[2]-1,1,1)).first()
                        if(saldoAnterior!=None):
                            activoTotalAnterior += float(saldoAnterior.monto_saldo)
                        #anexar ese saldo a una lista de saldos de activos corrientes
                        ActivoCorrienteMonto.append(valor)
                        #sumar el saldo
                        totalActivosCorriente += valor.monto_saldo
                    elif(cuentaObtenida.tipo_cuenta=="Activo no Corriente" or cuentaObtenida.tipo_cuenta=="Activo\xa0no\xa0Corriente"):
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
                            return mostrarMensajeSegunRol(request, "Error:No existe el balance general", idempresadmin)
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
                        saldoAnterior = SaldoDeCuentaBalace.objects.filter(idCuenta=cuentaObtenida.idCuenta,year_saldo=datetime(registro[2]-1,1,1)).first()
                        if(saldoAnterior!=None):
                            activoTotalAnterior += float(saldoAnterior.monto_saldo)
                        ActivoNoCorrienteMonto.append(valor)
                        totalActivosNoCorriente+=valor.monto_saldo
                    elif(cuentaObtenida.tipo_cuenta=="Pasivo Corriente" or cuentaObtenida.tipo_cuenta=="Pasivo\xa0Corriente"):
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
                            return mostrarMensajeSegunRol(request, "Error:No existe el balance general", idempresadmin)
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
                    elif(cuentaObtenida.tipo_cuenta=="Pasivo no Corriente" or cuentaObtenida.tipo_cuenta=="Pasivo\xa0no\xa0Corriente"):
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
                            return mostrarMensajeSegunRol(request, "Error:No existe el balance general", idempresadmin)
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
                            return mostrarMensajeSegunRol(request, "Error:No existe el balance general", idempresadmin)
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
                                montoAnteriorCuenta=cuentaAnterior.monto_saldo
                                if(montoAnteriorCuenta==0):
                                    porcentajeHorizontal = 0
                                else:
                                    porcentajeHorizontal = cuentaActual.monto_saldo/float(montoAnteriorCuenta) - 1
                                variacionHorizontal = cuentaActual.monto_saldo - float(montoAnteriorCuenta)
                                porcentajeVertical = cuentaActual.monto_saldo / totalActivos
                                linea=LineaDeInforme(
                                    idCuenta=cuentaActual.idCuenta,
                                    idAnalisis=anali,
                                    variacion_horizontal = round(float(variacionHorizontal),2),
                                    porcentaje_horizontal = round(float(porcentajeHorizontal),4),
                                    porcentaje_vertical = round(float(porcentajeVertical),4),
                                )
                                LineasActivos.append(linea)
                                linea.save()
                    for cuentaActual in montosPasivoCapital:
                        for cuentaAnterior in cuentasBalanceAnalisisAnt:
                            variacionHorizontal = 0.0
                            porcentajeHorizontal = 0.0
                            porcentajeVertical = 0.0
                            if(cuentaActual.idCuenta == cuentaAnterior.idCuenta):
                                montoAnteriorCuenta=cuentaAnterior.monto_saldo
                                if(montoAnteriorCuenta==0):
                                    porcentajeHorizontal = 0
                                else:
                                    porcentajeHorizontal = cuentaActual.monto_saldo/float(montoAnteriorCuenta) - 1
                                variacionHorizontal = cuentaActual.monto_saldo - float(montoAnteriorCuenta)
                                porcentajeVertical = cuentaActual.monto_saldo / (totalPasivos + totalCapital)
                                linea=LineaDeInforme(
                                    idCuenta=cuentaActual.idCuenta,
                                    idAnalisis=anali,
                                    variacion_horizontal = round(float(variacionHorizontal),2),
                                    porcentaje_horizontal = round(float(porcentajeHorizontal),4),
                                    porcentaje_vertical = round(float(porcentajeVertical),4),
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
                                if(cuentaAnterior.monto_saldo_Resul==0):
                                    porcentajeHorizontal = 0
                                else:
                                    porcentajeHorizontal = cuentaActual.monto_saldo_Resul/float(cuentaAnterior.monto_saldo_Resul) - 1
                                variacionHorizontal = cuentaActual.monto_saldo_Resul - float(cuentaAnterior.monto_saldo_Resul)
                                porcentajeVertical = cuentaActual.monto_saldo_Resul / ventasNetas
                                linea=LineaDeInforme(
                                    idCuenta=cuentaActual.idCuenta,
                                    idAnalisis=anali,
                                    variacion_horizontal = round(float(variacionHorizontal),2),
                                    porcentaje_horizontal = round(float(porcentajeHorizontal),4),
                                    porcentaje_vertical = round(float(porcentajeVertical),4),
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
                    if len(estadoOrdenadosVertical) != 0:
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
                    if len(estadoOrdenadosVertical) != 0:
                        mayorVariacionEstadoHorizontal= estadoOrdenadosHorizontal[0].idCuenta.nombre_cuenta
                        mayorPorcentajeEstadoHorizontal = estadoOrdenadosHorizontal[0].porcentaje_vertical*100
                    cadenaHorizontal = "La mayor variación con respecto al año pasado, se presenta en los " + activosOrdenadosHorizontal[0].idCuenta.tipo_cuenta + " siendo la cuenta " + mayorVariacionActivoHorizontal + " la que presenta la mayor variación con un " + str(mayorPorcentajeActivoHorizontal) + str(chr(37)) + ". "
                    cadenaHorizontal += "Por otro lado la mayor variación de la empresa se presentó en " + mayorVariacionCapitalHorizontal + " con una variación del " + str(mayorPorcentajeCapitalHorizontal) + str(chr(37)) + ". "
                    cadenaHorizontal += "Mientras que, las inversiones de terceros tuvieron su mayor variación en " + mayorVariacionPasivoHorizontal + " con un " + str(mayorPorcentajePasivoHorizontal) + str(chr(37)) + " con respecto al año pasado. "
                    if len(estadoOrdenadosVertical) != 0:
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
                    if promedioInventario != 0:
                        razonRotacionInventario = costoVentas / promedioInventario
                    if costoVentas != 0:
                        diasInventario = promedioInventario / (costoVentas/365)
                    promedioCuentasPorCobrar = (cuentasPorCobrar + cuentasPorCobraranterior) / 2
                    if promedioCuentasPorCobrar != 0:
                        razonRotacionCobros = ventasNetas / promedioCuentasPorCobrar
                    if ventasNetas != 0:
                        periodoMedioCobranza =promedioCuentasPorCobrar * 365 / ventasNetas
                    promedioCuentasPorPagar = (cuentasPorPagar + cuentasPorPagaranterior) / 2
                    if promedioCuentasPorPagar !=0:
                        razonRotacionPagos = (costoVentas - inventario) / promedioCuentasPorPagar
                    if costoVentas !=0 and inventario !=0:
                        periodoMedioPagos = promedioCuentasPorPagar * 365 / (costoVentas - inventario)
                    promedioActivoTotal = (activoTotalAnterior + totalActivos) / 2
                    if promedioActivoTotal !=0:
                        razonRotacionActivosTotales = ventasNetas / promedioActivoTotal
                    promedioActivoFijo = (activoFijo + activoFijoAnterior) / 2
                    if promedioActivoFijo !=0:
                        razonRotacionActivosFijos = ventasNetas/promedioActivoFijo
                    utilidadBruta = ventasNetas - costoVentas
                    utilidadOperativa = utilidadBruta - costoOperacion - gastoFinanciero
                    utilidadAntesImpuesto = utilidadOperativa + otrosIngresos - otrosGastos
                    utilidadNeta = utilidadAntesImpuesto - impuesto
                    if ventasNetas != 0:
                        indiceMargenBruto = utilidadBruta / ventasNetas
                        indiceMargenOperativo = utilidadOperativa /ventasNetas
                    if totalActivos !=0:
                        gradoEndeudamiento = totalPasivos / totalActivos
                        gradoPropiedad = totalCapital / totalActivos
                    if totalCapital !=0:
                        endeudamientoPatrimonial = totalPasivos / totalCapital
                    if gastoFinanciero != 0:
                        coberturaGastosFinancieros = utilidadAntesImpuesto / gastoFinanciero
                    ratios=[]
                    ratios.append(razonLiquidezCorriente)
                    ratios.append(razonLiquidezRapida)
                    ratios.append(razonCapitalTrabajo)
                    ratios.append(razonEfectivo)
                    ratios.append(razonRotacionInventario)
                    ratios.append(diasInventario)
                    ratios.append(razonRotacionCobros)
                    ratios.append(periodoMedioCobranza)
                    ratios.append(razonRotacionPagos)
                    ratios.append(periodoMedioPagos)
                    ratios.append(razonRotacionActivosTotales)
                    ratios.append(razonRotacionActivosFijos)
                    ratios.append(indiceMargenBruto)
                    ratios.append(indiceMargenOperativo)
                    ratios.append(gradoEndeudamiento)
                    ratios.append(gradoPropiedad)
                    ratios.append(endeudamientoPatrimonial)
                    ratios.append(coberturaGastosFinancieros)
                    RatioUltimo = None
                    #Inicializa variables de id a cero
                    IdRatioUltimo = 0
                    try:
                        #Obtener el último Balance ingresado
                        RatioUltimo = RatiosAnalisis.objects.latest('idRatioAnalisis')
                    #Si no existe
                    except RatiosAnalisis.DoesNotExist:
                        #Asegurarse que sea None
                        RatioUltimo = None
                    #Si el último balance no existe
                    if(RatioUltimo==None):
                        #Definir el Id como 1
                        IdRatioUltimo = 1
                    else:
                        #Caso contrario, tomar el id del último balance y sumar 1
                        IdRatioUltimo = RatioUltimo.idRatioAnalisis + 1
                    for ratio in enumerate(ratios):
                        ratioanalisis=None
                        RatioActual = Ratios.objects.filter(idRatio=int(ratio[0]) + 1).first()
                        ratioanalisis = RatiosAnalisis(
                            idRatioAnalisis = IdRatioUltimo,
                            idAnalisis = anali,
                            idRatios = RatioActual,
                            valorRatiosAnalisis = float(ratio[1]),
                            conclusion = "",
                        )
                        #Se guarda el ratio
                        ratioanalisis.save()
                        #Se obtiene el giro actual
                        GiroActual = empresaActual.idGiro
                        #Se traen las empresas del giro actual
                        EmpresasDelGiro = Empresa.objects.filter(idGiro = GiroActual.idGiro)
                        #Se obtienen todos los detalles de ratios de todas las empresas del ratio actual
                        DetallesDelRatioActual = RatiosAnalisis.objects.filter(idRatios = RatioActual.idRatio)
                        sumatoria=0.0
                        cantidad=0
                        promedio=0
                        for detalle in DetallesDelRatioActual:
                            for empresaGiro in EmpresasDelGiro:
                                #Si es detalle del ratio actual de una empresa del giro actual
                                if(detalle.idAnalisis.idEmpresa == empresaGiro):
                                    #sumatoria general
                                    sumatoria=sumatoria+float(detalle.valorRatiosAnalisis)
                                    #contador
                                    cantidad=cantidad+1
                        if(cantidad!=0):
                            promedio = sumatoria / cantidad
                        else:
                            promedio = 0
                        #Se obtiene el dato de giro del giro actual y ratio actual
                        DatoGiroActual = DatoGiro.objects.filter(idGiro = GiroActual.idGiro, idRatio = RatioActual.idRatio).first()
                        UltimoDatoGiro = None
                        #Inicializa variables de id a cero
                        IdUltimoDatoGiro = 0
                        try:
                            #Obtener el último Balance ingresado
                            UltimoDatoGiro = DatoGiro.objects.latest('idDato')
                        #Si no existe
                        except DatoGiro.DoesNotExist:
                            #Asegurarse que sea None
                            UltimoDatoGiro = None
                        #Si el último balance no existe
                        if(UltimoDatoGiro==None):
                            #Definir el Id como 1
                            IdUltimoDatoGiro = 1
                        else:
                            #Caso contrario, tomar el id del último balance y sumar 1
                            IdUltimoDatoGiro = UltimoDatoGiro.idDato + 1
                        if(DatoGiroActual==None):
                            datosDeGiro = DatoGiro(
                                idDato = IdUltimoDatoGiro,
                                idGiro = GiroActual,
                                idRatio = RatioActual,
                                valorParametro = 0,
                                valorPromedio = promedio,
                            )
                            datosDeGiro.save()
                        else:
                            datosDeGiro = DatoGiro(
                                idDato = DatoGiroActual.idDato,
                                idGiro = GiroActual,
                                idRatio = RatioActual,
                                valorParametro = DatoGiroActual.valorParametro,
                                valorPromedio = promedio,
                            )
                            datosDeGiro.save()
                        IdRatioUltimo = IdRatioUltimo + 1                
                exito="Se agregaron los saldos correctamente"
                return mostrarMensajeSegunRol(request, exito, idempresadmin)
            ###############POST SIN ARCHIVOS################
            #para request post sin archivos, obtendrá el form
            else:
                #Usando la request POST, crear un formulario de tipo EstadoForm
                formulario=EstadoForm(request.POST)
                #Si el form POSTeado es válido (pendiente de modificar is_valid)
                if(formulario.is_valid()):
                    #Obtiene todos los balances de la empresa
                    BalancesEmpresa = BalanceEmpresa.objects.filter(idEmpresa=empresa).order_by('idbalance')
                    anioForm = formulario.data.get("yearEstado")
                    fechaInicioForm = formulario.data.get("fechaInicioBalance")
                    fechaInicioList = fechaInicioForm.split("-")
                    fechaFinForm = formulario.data.get("fechaFinBalance")
                    fechaFinList= fechaFinForm.split("-")
                    #Si el mes de fin de periodo es mayor al ombligo del año
                    if int(fechaFinList[1]) >= 6:
                        #y el año que se provee es mayor que el año de fin de periodo
                        if int(fechaFinList[0]) < int(anioForm):
                            #Error
                            return mostrarMensajeSegunRol(request, "El año provisto no puede ser mayor al fin del año", idempresadmin)
                    #Caso contrario si el mes es menor al ombligo de año pero el anio provisto + 2 es mayor al fin
                    elif int(fechaFinList[1]) < 6 and int(fechaFinList[0])<=int(anioForm) + 2:
                            return mostrarMensajeSegunRol(request, "El año provisto no puede ser mayor al fin del año", idempresadmin)
                    if int(fechaInicioList[0])<int(anioForm):
                        return mostrarMensajeSegunRol(request, "El año provisto no puede ser mayor al inicio del año", idempresadmin)
                    if int(fechaInicioList[0])>int(anioForm)+2:
                        return mostrarMensajeSegunRol(request, "El año provisto no puede ser mayor al inicio del año", idempresadmin)

                    #Luz verde para empezar a insertar
                    LuzVerde = True
                    #Para cada estado de la empresa
                    for balance in BalancesEmpresa:
                        #Si el estado es del año dado
                        if(str(balance.idbalance.yearEstado)==str(anioForm)):
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
                        return mostrarMensajeSegunRol(request, exito, idempresadmin)
                    else:
                        exito="No se inserto ha podido insertar el estado, ya existe."
                        return mostrarMensajeSegunRol(request, exito, idempresadmin)
            #para ambos posts
            argumentos = {}
        #############REQUEST GET#################33
        #Para request get
        else:
            formulario=EstadoForm()
            argumentos = {
                "idEmpresaActual":empresa,
                "ListaBalances":empresaActual.BalancesDeEmpresa.all(),
                "formIngresarEstado":EstadoForm(),
                'esGerente':esGerente
            }
            return render(request, 'Estados/EstadosIndex.html',argumentos)
    else:
        return render(request, 'Usuarios/Error401.html')

# Create your views here.
def indexEstadoResultado(request, anio, idempresadmin = None):
    #define el codigo del form para los accesos
    op = '005'
    #obtiene el usuario de la sesión actual
    idUsuarioActual = request.user.id
    idRolUsuarioActual = request.user.rol
    #obtiene la tupla de acceso del usuario actual al form actual
    usac=AccesoUsuario.objects.filter(idUsuario=idUsuarioActual,idOpcion=op).first()
    esGerente=False
    #Si el acceso existe
    if(usac!=None):
        if(idRolUsuarioActual==3):
            empresaActual=get_object_or_404(Empresa,gerente=idUsuarioActual)
            esGerente = True
        else:
            empresaActual=Empresa.objects.filter(idEmpresa=idempresadmin).first()
            esGerente = False
            if(empresaActual==None):
                 raise Http404("Oops, esta página no existe.")
        empresa = empresaActual.idEmpresa
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
            if(cuenta.tipo_cuenta=="Estado de Resultado" or cuenta.tipo_cuenta=='Estado\xa0de\xa0Resultado'):
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
            'empresaid':empresa,
            'esGerente':esGerente
        }
        return render(request,'Estados/EstadoResultados.html', argumentos)
    else:
        return render(request, 'Usuarios/Error401.html')

# Index de balance general
def indexBalanceGeneral(request, anio, idempresadmin = None):
    #define el codigo del form para los accesos
    op = '005'
    #obtiene el usuario de la sesión actual
    idUsuarioActual = request.user.id
    idRolUsuarioActual = request.user.rol
    #obtiene la tupla de acceso del usuario actual al form actual
    usac=AccesoUsuario.objects.filter(idUsuario=idUsuarioActual,idOpcion=op).first()
    esGerente=False
    #Si el acceso existe
    if(usac!=None):
        if(idRolUsuarioActual==3):
            empresaActual=get_object_or_404(Empresa,gerente=idUsuarioActual)
            esGerente = True
        else:
            empresaActual=Empresa.objects.filter(idEmpresa=idempresadmin).first()
            esGerente=False
            if(empresaActual==None):
                 raise Http404("Oops, esta página no existe.")
        empresa = empresaActual.idEmpresa
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
            if(cuenta.tipo_cuenta!="Estado de Resultado" or cuenta.tipo_cuenta!='Estado\xa0de\xa0Resultado'):
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
            'empresaid':idempresadmin,
            'esGerente':esGerente
        }
        return render(request,'Estados/BalanceGeneral.html', argumentos)
    else:
        return render(request, 'Usuarios/Error401.html')

def mensajeRedireccion(request,mensaje,empresaidmen=None):
    if(request.user.rol==3):
        return render(request,'Estados/mensajeRedireccion.html', {'mensaje':mensaje,'esGerente':True})
    else:
        return render(request,'Estados/mensajeRedireccion.html', {'mensaje':mensaje,'empresa':empresaidmen, 'esGerente':False})

def nuevoEditarSaldo(request,tipoCuenta,accion=None, idempresadmin = None):
    if request.user.is_authenticated:
        #define el codigo del form para los accesos
        op = '005'
        #obtiene el usuario de la sesión actual
        idUsuarioActual = request.user.id
        idRolUsuarioActual = request.user.rol
        #obtiene la tupla de acceso del usuario actual al form actual
        usac=AccesoUsuario.objects.filter(idUsuario=idUsuarioActual,idOpcion=op).first()
        esGerente=False
        #Si el acceso existe
        if(usac!=None):
            if(idRolUsuarioActual==3):
                empresaActual=get_object_or_404(Empresa,gerente=idUsuarioActual)
                esGerente = True
            else:
                empresaActual=Empresa.objects.filter(idEmpresa=idempresadmin).first()
                esGerente=False
                if(empresaActual==None):
                    #La empresa no se encontró: Not Found 404
                    raise Http404("La empresa actual no existe, este mensaje fue levantado al acceder como administrador.")
            empresa = empresaActual.idEmpresa
            #Si recibe request GET
            if request.method == 'GET':
                if accion == "Nuevo":
                    if(tipoCuenta=="Balance" or tipoCuenta=="Estado"):
                        #ingresar nuevo
                        argumentos = {
                            'tipoEstado':tipoCuenta,
                            'listaCuentas':obtenerCuentas(tipoCuenta,empresa),
                            'listaEstados':obtenerEstados(tipoCuenta,empresa),
                            'formulario':SaldoCuentaForm(empresa),
                            'accion':accion,
                            'esGerente':esGerente,
                            'empresa':idempresadmin
                        }
                        return render(request,'Estados/nuevoeditarsaldo.html',argumentos)
                    else:
                        raise Http404("No se ha provisto un tipo de cuenta correcto")
                else:
                    raise Http404
            #Si recibe request POST
            else:
                #Si se va a mostrar el formulario para editar
                if accion == "Editar":
                    idsal = request.POST.get('saldoid')
                    saldoAux = None
                    estadoAux=None
                    montoAux = None
                    if tipoCuenta == "Balance":
                        saldoAux = SaldoDeCuentaBalace.objects.get(idSaldo=idsal)
                        idbal = request.POST.get('balanceid')
                        estadoAux = Balance.objects.get(idBalance=idbal)
                        listadoEstadoSalida = [(estadoAux.idBalance,'Balance general del ' + str(estadoAux.yearEstado))]
                        montoAux = saldoAux.monto_saldo
                    elif tipoCuenta=="Estado":
                        saldoAux = SaldoDeCuentaResultado.objects.get(idSaldoResul=idsal)
                        idres = request.POST.get('resultadoid')
                        estadoAux=EstadoDeResultado.objects.get(idResultado=idres)
                        listadoEstadoSalida = [(estadoAux.idResultado,'Estado de Resultados del ' + str(estadoAux.yearEstado))]
                        montoAux = saldoAux.monto_saldo_Resul
                    else:
                        raise Http404
                    listadoCuentasSalida = obtenerCuentas(tipoCuenta,empresa)
                    cuentaFinal = []
                    for cuenta in listadoCuentasSalida:
                        if cuenta[0] == saldoAux.idCuenta.idCuenta:
                            cuentaFinal.append(cuenta)
                    argumentos = {
                        'tipoEstado':tipoCuenta,
                        'listaCuentas':cuentaFinal,
                        'listaEstados':listadoEstadoSalida,
                        'formulario':SaldoCuentaForm(empresa),
                        'accion':accion,
                        'empresa':empresa,
                        'esGerente':esGerente,
                        'idsal':idsal,
                        'monto':montoAux
                    }
                    return render(request,'Estados/nuevoeditarsaldo.html',argumentos)
                #Si se esta posteando el form
                elif accion == None:
                    anioAnalisis = None
                    mensajeSalida=""
                    if request.POST.get('tipoForm')=='Nuevo':
                        ultimoSaldo = None
                        idUltimoSaldo=0
                        anioSaldo = 0
                        cuentaRecibida = request.POST.get('Cuenta')
                        cuentaSalida=Cuenta.objects.get(idCuenta=cuentaRecibida)
                        estadoRecibido = request.POST.get('Estado')
                        estado = None
                        if tipoCuenta=="Balance":
                            estado=Balance.objects.get(idBalance=estadoRecibido)
                            saldosDelBalance = SaldoDeCuentaBalace.objects.filter(idCuenta=cuentaSalida.idCuenta,idbalance=estadoRecibido)
                            if(saldosDelBalance.count()==0):
                                try:
                                    ultimoSaldo = SaldoDeCuentaBalace.objects.latest('idSaldo')
                                    idUltimoSaldo=ultimoSaldo.idSaldo
                                except:
                                    idUltimoSaldo=0
                                anioSaldo = estado.yearEstado
                                montoRecibido = request.POST.get('Monto')
                                saldoSalida = SaldoDeCuentaBalace(
                                    idSaldo = int(idUltimoSaldo) + 1,
                                    idCuenta = cuentaSalida,
                                    idbalance = estado,
                                    year_saldo = datetime(int(anioSaldo),1,1),
                                    monto_saldo = round(float(montoRecibido),2)
                                )
                            else:
                                saldoSalida = SaldoDeCuentaBalace.objects.filter(idCuenta=saldosDelBalance.first().idCuenta.idCuenta,idbalance=estadoRecibido).first()
                                anioSaldo = estado.yearEstado
                                montoRecibido = request.POST.get('Monto')
                                saldoSalida = SaldoDeCuentaBalace(
                                    idSaldo = saldoSalida.idSaldo,
                                    idCuenta = saldoSalida.idCuenta,
                                    idbalance = saldoSalida.idbalance,
                                    year_saldo = saldoSalida.year_saldo,
                                    monto_saldo = round(float(montoRecibido),2)
                                )
                        else:
                            estado=EstadoDeResultado.objects.get(idResultado=estadoRecibido)
                            saldosDelResultado = SaldoDeCuentaResultado.objects.filter(idCuenta=cuentaSalida.idCuenta,idResultado=estadoRecibido)
                            if(saldosDelResultado.count()==0):
                                try:
                                    ultimoSaldo = SaldoDeCuentaResultado.objects.latest('idSaldoResul')
                                    idUltimoSaldo=ultimoSaldo.idSaldoResul
                                except:
                                    idUltimoSaldo=0
                                anioSaldo = estado.yearEstado
                                montoRecibido = request.POST.get('Monto')
                                saldoSalida = SaldoDeCuentaResultado(
                                    idSaldoResul = int(idUltimoSaldo) + 1,
                                    idCuenta = cuentaSalida,
                                    idResultado = estado,
                                    year_saldo_Resul = datetime(int(anioSaldo),1,1),
                                    monto_saldo_Resul = round(float(montoRecibido),2)
                                )
                            else:
                                saldoSalida = SaldoDeCuentaResultado.objects.filter(idCuenta=saldosDelResultado.first().idCuenta.idCuenta,idResultado=estadoRecibido).first()
                                anioSaldo = estado.yearEstado
                                montoRecibido = request.POST.get('Monto')
                                saldoSalida = SaldoDeCuentaResultado(
                                    idSaldoResul = saldoSalida.idSaldoResul,
                                    idCuenta = saldoSalida.idCuenta,
                                    idResultado = saldoSalida.idResultado,
                                    year_saldo_Resul = saldoSalida.year_saldo_Resul,
                                    monto_saldo_Resul = round(float(montoRecibido),2)
                                )
                        saldoSalida.save()
                        mensajeSalida="El saldo se añadió correctamente."
                    else:
                        idSaldo = request.POST.get('idsal')
                        cuentaRecibida = request.POST.get('Cuenta')
                        cuentaSalida=Cuenta.objects.get(idCuenta=cuentaRecibida)
                        estadoRecibido = request.POST.get('Estado')
                        montoRecibido = request.POST.get('Monto') 
                        if tipoCuenta=="Balance":
                            estado=Balance.objects.get(idBalance=estadoRecibido)
                            anioSaldo = estado.yearEstado
                            saldoSalida = SaldoDeCuentaBalace(
                                idSaldo = idSaldo,
                                idCuenta = cuentaSalida,
                                idbalance = estado,
                                year_saldo = datetime(int(anioSaldo),1,1),
                                monto_saldo = round(float(montoRecibido),2)
                            )  
                        else:
                            estado=EstadoDeResultado.objects.get(idResultado=estadoRecibido)
                            anioSaldo = estado.yearEstado
                            saldoSalida = SaldoDeCuentaResultado(
                                idSaldoResul = idSaldo,
                                idCuenta = cuentaSalida,
                                idResultado = estado,
                                year_saldo_Resul = datetime(int(anioSaldo),1,1),
                                monto_saldo_Resul = round(float(montoRecibido),2)
                            )
                        saldoSalida.save()          
                        mensajeSalida="El saldo se edito correctamente."   
                    ###########PROCESO ANALISIS###############
                    anioAnalisis = anioSaldo
                    if(anioAnalisis==0):
                        UltimoBalance = BalanceEmpresa.objects.filter(idEmpresa=empresa).latest('idbalance')
                        anioAnalisis=UltimoBalance.idbalance.yearEstado
                    analisisActual = Analisis.objects.filter(year_analisis=anioAnalisis, idEmpresa=empresa)
                    if(analisisActual.first() == None):
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
                            ActivoCorrienteMonto = []
                            ActivoNoCorrienteMonto = []
                            PasivoCorrienteMonto = []
                            PasivoNoCorrienteMonto = []
                            CapitalMonto = []
                            EstadosDeResultadosMonto = []
                            ventasNetas=0.0
                            totalActivosCorriente = 0.0
                            totalActivosNoCorriente = 0.0
                            totalPasivosCorriente = 0.0
                            totalPasivosNoCorriente = 0.0
                            totalCapital=0.0
                            activosCortoPlazo=0.0
                            costoVentas=0.0
                            cuentasPorCobrar=0.0
                            cuentasPorPagar=0.0
                            activoFijo = 0.0
                            costoOperacion = 0.0
                            gastoFinanciero = 0.0
                            otrosGastos=0.0
                            otrosIngresos=0.0
                            impuesto=0.0
                            activoTotalAnterior=0.0
                            cuentasEmpresa = Cuenta.objects.filter(idEmpresa=empresa)
                            esEstado = True
                            for cuenta in cuentasEmpresa:     
                                if cuenta.tipo_cuenta== "Estado de Resultado" or cuenta.tipo_cuenta == "Estado\xa0de\xa0Resultado":
                                    valor=SaldoDeCuentaResultado.objects.filter(idCuenta=cuenta.idCuenta,idResultado=estadoAnalisis.idResultado).first()  
                                    valorAnterior=SaldoDeCuentaResultado.objects.filter(idCuenta=cuenta.idCuenta,idResultado=estadoAnterior.idResultado).first()  
                                else:
                                    valor=SaldoDeCuentaBalace.objects.filter(idCuenta=cuenta.idCuenta,idbalance=balanceAnalisis.idBalance).first()
                                    valorAnterior=SaldoDeCuentaBalace.objects.filter(idCuenta=cuenta.idCuenta,idbalance=balanceAnterior.idBalance).first()
                                    esEstado = False    
                                if(cuenta.idSobreNombre != None):            
                                    if(cuenta.idSobreNombre.sobreNombre=="Inventario"):
                                        if(esEstado == True):
                                            inventario = float(valor.monto_saldo_Resul)
                                        else:
                                            inventario = float(valor.monto_saldo)
                                        try:
                                            inventarioAnteriorObj = SaldoDeCuentaBalace.objects.get(idCuenta=cuenta.idCuenta,year_saldo_Resul=datetime(anioAnalisis-1,1,1))
                                            inventarioAnterior=float(inventarioAnteriorObj.monto_saldo)
                                        except:
                                            inventarioAnterior = 0
                                    elif(cuenta.idSobreNombre.sobreNombre=="Activo de corto plazo"):
                                        if esEstado == True:
                                            activosCortoPlazo+=float(valor.monto_saldo_Resul)
                                        else:
                                            activosCortoPlazo+=float(valor.monto_saldo)
                                    elif(cuenta.idSobreNombre.sobreNombre=="Costo de servicio o ventas"):
                                        if esEstado==True:
                                            costoVentas+=float(valor.monto_saldo_Resul)
                                        else:
                                            costoVentas+=float(valor.monto_saldo)
                                    elif(cuenta.idSobreNombre.sobreNombre=="Cuenta por cobrar"):
                                        if esEstado==True:
                                            cuentasPorCobrar+=float(valor.monto_saldo_Resul)
                                        else:
                                            cuentasPorCobrar+=float(valor.monto_saldo)
                                        try:
                                            cuentasPorCobraranteriorObj=SaldoDeCuentaBalace.objects.get(idCuenta=cuenta.idCuenta,year_saldo_Resul=datetime(anioAnalisis-1,1,1))
                                            cuentasPorCobraranterior=float(cuentasPorCobraranteriorObj.monto_saldo)
                                        except:
                                            cuentasPorCobraranterior=0      
                                    elif(cuenta.idSobreNombre.sobreNombre=="Cuenta por pagar"):
                                        if esEstado==True:
                                            cuentasPorPagar+=float(valor.monto_saldo_Resul)
                                        else:
                                            cuentasPorPagar+=float(valor.monto_saldo)
                                        try:
                                            cuentasPorPagaranteriorObj = SaldoDeCuentaBalace.objects.get(idCuenta=cuenta.idCuenta,year_saldo_Resul=datetime(anioAnalisis-1,1,1))
                                            cuentasPorPagaranterior = float(cuentasPorPagaranteriorObj.monto_saldo)
                                        except:
                                            cuentasPorPagaranterior = 0                  
                                    elif(cuenta.idSobreNombre.sobreNombre=="Ventas netas"):
                                        if esEstado==True:
                                            ventasNetas+=float(valor.monto_saldo_Resul)
                                        else:
                                            ventasNetas+=float(valor.monto_saldo)
                                    elif(cuenta.idSobreNombre.sobreNombre=="Activo Fijo"):
                                        if esEstado==True:
                                            activoFijo+=float(valor.monto_saldo_Resul)
                                        else:
                                            activoFijo+=float(valor.monto_saldo)
                                        try:
                                            activoFijoAnteriorObj = SaldoDeCuentaBalace.objects.get(idCuenta=cuenta.idCuenta,year_saldo_Resul=datetime(anioAnalisis-1,1,1))
                                            activoFijoAnterior = float(activoFijoAnteriorObj.monto_saldo)
                                        except:
                                            activoFijoAnterior=0
                                    elif(cuenta.idSobreNombre.sobreNombre=="Costo de operación o administración"):
                                        if esEstado==True:
                                            costoOperacion+=float(valor.monto_saldo_Resul)
                                        else:
                                            costoOperacion+=float(valor.monto_saldo)
                                    elif(cuenta.idSobreNombre.sobreNombre=="Gastos financieros"):
                                        if esEstado==True:
                                            gastoFinanciero+=float(valor.monto_saldo_Resul)
                                        else:
                                            gastoFinanciero+=float(valor.monto_saldo)
                                    elif(cuenta.idSobreNombre.sobreNombre=="Otros gastos"):
                                        if esEstado==True:
                                            otrosGastos+=float(valor.monto_saldo_Resul)
                                        else:
                                            otrosGastos+=float(valor.monto_saldo)
                                    elif(cuenta.idSobreNombre.sobreNombre=="Otros ingresos"):
                                        if esEstado==True:
                                            otrosIngresos+=float(valor.monto_saldo_Resul)
                                        else:
                                            otrosIngresos+=float(valor.monto_saldo)
                                    elif(cuenta.idSobreNombre.sobreNombre=="Impuestos"):
                                        if esEstado==True:
                                            impuesto+=float(valor.monto_saldo_Resul)
                                        else:
                                            impuesto+=float(valor.monto_saldo)
                                if(cuenta.tipo_cuenta=="Activo Corriente" or cuenta.tipo_cuenta=="Activo\xa0Corriente"):
                                    ActivoCorrienteMonto.append(valor)
                                    totalActivosCorriente = totalActivosCorriente + valor.monto_saldo
                                    activoTotalAnterior= activoTotalAnterior + valor.monto_saldo
                                elif(cuenta.tipo_cuenta=="Activo no Corriente" or cuenta.tipo_cuenta=="Activo\xa0no\xa0Corriente"):
                                    ActivoNoCorrienteMonto.append(valor)
                                    totalActivosNoCorriente = totalActivosNoCorriente + valor.monto_saldo
                                    activoTotalAnterior = activoTotalAnterior + valor.monto_saldo
                                if(cuenta.tipo_cuenta=="Pasivo Corriente" or cuenta.tipo_cuenta=="Pasivo\xa0Corriente"):
                                    PasivoCorrienteMonto.append(valor)
                                    totalPasivosCorriente = totalPasivosCorriente + valor.monto_saldo
                                elif(cuenta.tipo_cuenta=="Pasivo no Corriente" or cuenta.tipo_cuenta=="Pasivo\xa0no\xa0Corriente"):
                                    PasivoNoCorrienteMonto.append(valor)
                                    totalPasivosNoCorriente = totalPasivosNoCorriente + valor.monto_saldo
                                elif(cuenta.tipo_cuenta=="Capital"):
                                    CapitalMonto.append(valor)
                                    totalCapital = totalCapital + valor.monto_saldo
                                elif(cuenta.tipo_cuenta=="Estado de Resultado" or cuenta.tipo_cuenta=="Estado\xa0de\xa0Resultado"):
                                    EstadosDeResultadosMonto.append(valor)
                                    if(cuenta.idSobreNombre.sobreNombre=="Ventas netas"):
                                        ventasNetas=valor.monto_saldo_Resul
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
                            totalActivos = totalActivosCorriente + totalActivosNoCorriente
                            totalPasivos = totalPasivosCorriente + totalPasivosNoCorriente
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
                                            variacion_horizontal = round(float(variacionHorizontal),2),
                                            porcentaje_horizontal = round(float(porcentajeHorizontal),4),
                                            porcentaje_vertical = round(float(porcentajeVertical),4),
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
                                            variacion_horizontal = round(float(variacionHorizontal),2),
                                            porcentaje_horizontal = round(float(porcentajeHorizontal),4),
                                            porcentaje_vertical = round(float(porcentajeVertical),4),
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
                                            variacion_horizontal = round(float(variacionHorizontal),2),
                                            porcentaje_horizontal = round(float(porcentajeHorizontal),4),
                                            porcentaje_vertical = round(float(porcentajeVertical),4),
                                        )
                                        LineasEstados.append(linea)
                                        linea.save()
                                    else:
                                        porcentajeHorizontal = cuentaActual.monto_saldo_Resul/float(cuentaAnterior.monto_saldo_Resul) - 1
                                        variacionHorizontal = cuentaActual.monto_saldo_Resul - float(cuentaAnterior.monto_saldo_Resul)
                                        porcentajeVertical = 0.0
                                        linea=LineaDeInforme(
                                            idCuenta=cuentaActual.idCuenta,
                                            idAnalisis=anali,
                                            variacion_horizontal = round(float(variacionHorizontal),2),
                                            porcentaje_horizontal = round(float(porcentajeHorizontal),4),
                                            porcentaje_vertical = round(float(porcentajeVertical),4),
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
                            ratios=[]
                            ratios.append(razonLiquidezCorriente)
                            ratios.append(razonLiquidezRapida)
                            ratios.append(razonCapitalTrabajo)
                            ratios.append(razonEfectivo)
                            ratios.append(razonRotacionInventario)
                            ratios.append(diasInventario)
                            ratios.append(razonRotacionCobros)
                            ratios.append(periodoMedioCobranza)
                            ratios.append(razonRotacionPagos)
                            ratios.append(periodoMedioPagos)
                            ratios.append(razonRotacionActivosTotales)
                            ratios.append(razonRotacionActivosFijos)
                            ratios.append(indiceMargenBruto)
                            ratios.append(indiceMargenOperativo)
                            ratios.append(gradoEndeudamiento)
                            ratios.append(gradoPropiedad)
                            ratios.append(endeudamientoPatrimonial)
                            ratios.append(coberturaGastosFinancieros)
                            RatioUltimo = None
                            #Inicializa variables de id a cero
                            IdRatioUltimo = 0
                            try:
                                #Obtener el último Balance ingresado
                                RatioUltimo = RatiosAnalisis.objects.latest('idRatioAnalisis')
                            #Si no existe
                            except RatiosAnalisis.DoesNotExist:
                                #Asegurarse que sea None
                                RatioUltimo = None
                            #Si el último balance no existe
                            if(RatioUltimo==None):
                                #Definir el Id como 1
                                IdRatioUltimo = 1
                            else:
                                #Caso contrario, tomar el id del último balance y sumar 1
                                IdRatioUltimo = RatioUltimo.idRatioAnalisis + 1
                            for ratio in enumerate(ratios):
                                ratioanalisis=None
                                RatioActual = Ratios.objects.filter(idRatio=int(ratio[0]) + 1).first()
                                ratioanalisis = RatiosAnalisis(
                                    idRatioAnalisis = IdRatioUltimo,
                                    idAnalisis = anali,
                                    idRatios = RatioActual,
                                    valorRatiosAnalisis = float(ratio[1]),
                                    conclusion = "",
                                )
                                #Se guarda el ratio
                                ratioanalisis.save()
                                #Se obtiene el giro actual
                                GiroActual = empresaActual.idGiro
                                #Se traen las empresas del giro actual
                                EmpresasDelGiro = Empresa.objects.filter(idGiro = GiroActual.idGiro)
                                #Se obtienen todos los detalles de ratios de todas las empresas del ratio actual
                                DetallesDelRatioActual = RatiosAnalisis.objects.filter(idRatios = RatioActual.idRatio)
                                sumatoria=0.0
                                cantidad=0
                                promedio=0
                                for detalle in DetallesDelRatioActual:
                                    for empresaGiro in EmpresasDelGiro:
                                        #Si es detalle del ratio actual de una empresa del giro actual
                                        if(detalle.idAnalisis.idEmpresa == empresaGiro):
                                            #sumatoria general
                                            sumatoria=sumatoria+float(detalle.valorRatiosAnalisis)
                                            #contador
                                            cantidad=cantidad+1
                                if(cantidad!=0):
                                    promedio = sumatoria / cantidad
                                else:
                                    promedio = 0
                                #Se obtiene el dato de giro del giro actual y ratio actual
                                DatoGiroActual = DatoGiro.objects.filter(idGiro = GiroActual.idGiro, idRatio = RatioActual.idRatio).first()
                                UltimoDatoGiro = None
                                #Inicializa variables de id a cero
                                IdUltimoDatoGiro = 0
                                try:
                                    #Obtener el último Balance ingresado
                                    UltimoDatoGiro = DatoGiro.objects.latest('idDato')
                                #Si no existe
                                except DatoGiro.DoesNotExist:
                                    #Asegurarse que sea None
                                    UltimoDatoGiro = None
                                #Si el último balance no existe
                                if(UltimoDatoGiro==None):
                                    #Definir el Id como 1
                                    IdUltimoDatoGiro = 1
                                else:
                                    #Caso contrario, tomar el id del último balance y sumar 1
                                    IdUltimoDatoGiro = UltimoDatoGiro.idDato + 1
                                if(DatoGiroActual==None):
                                    datosDeGiro = DatoGiro(
                                        idDato = IdUltimoDatoGiro,
                                        idGiro = GiroActual,
                                        idRatio = RatioActual,
                                        valorParametro = 0,
                                        valorPromedio = promedio,
                                    )
                                    datosDeGiro.save()
                                else:
                                    datosDeGiro = DatoGiro(
                                        idDato = DatoGiroActual.idDato,
                                        idGiro = GiroActual,
                                        idRatio = RatioActual,
                                        valorParametro = DatoGiroActual.valorParametro,
                                        valorPromedio = promedio,
                                    )
                                    datosDeGiro.save()
                                IdRatioUltimo = IdRatioUltimo + 1   
                    else:
                        analisisAuxiliar = analisisActual.first()
                        try:
                            ultimaLineaDeInforme=LineaDeInforme.objects.latest('idLineaInfo')
                            ultimoIdLinea = int(ultimaLineaDeInforme.idLineaInfo) + 1
                        except:
                            ultimoIdLinea = 1
                        cuentaAuxiliarTrabajo = Cuenta.objects.get(idCuenta=cuentaRecibida)
                        totalER = 0.0
                        totalActivo = 0.0
                        totalNoActivo = 0.0
                        porVert = 0.0
                        estadoEmp = EstadoEmpresa.objects.filter(idEmpresa=empresa)
                        for relacion in estadoEmp:
                            if relacion.idResultado.yearEstado == analisisAuxiliar.year_analisis:
                                estadoActl = relacion.idResultado
                        balancEmp = BalanceEmpresa.objects.filter(idEmpresa=empresa)
                        for relacion in balancEmp:
                            if relacion.idbalance.yearEstado == analisisAuxiliar.year_analisis:
                                balanceActl = relacion.idbalance
                        if cuentaAuxiliarTrabajo.tipo_cuenta == "Estado de Resultado" or cuentaAuxiliarTrabajo.tipo_cuenta == "Estado\xa0de\xa0Resultado":
                            for saldoCuenta in SaldoDeCuentaResultado.objects.filter(idResultado=estadoActl.idResultado,year_saldo_Resul=datetime(analisisAuxiliar.year_analisis,1,1)):
                                totalER = float(totalER) + float(saldoCuenta.monto_saldo_Resul)
                            if totalER != 0:
                                porVert = float(montoRecibido) / float(totalER)
                            else:
                                porVert = 0.0
                            saldoAnioanteriorTrabajo = SaldoDeCuentaResultado.objects.filter(idCuenta=cuentaRecibida, year_saldo_Resul = datetime(int(analisisAuxiliar.year_analisis)-1,1,1)).first()
                            if saldoAnioanteriorTrabajo == None:
                                saldoAnt = 0
                            else:
                                saldoAnt = saldoAnioanteriorTrabajo.monto_saldo_Resul
                            varHori = float(montoRecibido) - float(saldoAnt)
                            if(saldoAnt==0):
                                porHori = 1
                            else:
                                porHori = float(varHori) / float(saldoAnt)
                        elif cuentaAuxiliarTrabajo.tipo_cuenta == "Activo Corriente" or cuentaAuxiliarTrabajo.tipo_cuenta == "Activo\xa0Corriente" or cuentaAuxiliarTrabajo.tipo_cuenta == "Activo\xa0no\xa0Corriente" or cuentaAuxiliarTrabajo.tipo_cuenta == "Activo no Corriente":
                            for saldoCuenta in SaldoDeCuentaBalace.objects.filter(idbalance=balanceActl.idBalance,year_saldo=datetime(analisisAuxiliar.year_analisis,1,1)):
                                totalActivo = float(totalActivo) + float(saldoCuenta.monto_saldo)
                            if totalActivo != 0:
                                porVert = float(montoRecibido) / float(totalActivo)
                            else:
                                porVert = 0
                            saldoAnioanteriorTrabajo = SaldoDeCuentaBalace.objects.filter(idCuenta=cuentaRecibida, year_saldo = datetime(int(analisisAuxiliar.year_analisis)-1,1,1)).first()
                            if saldoAnioanteriorTrabajo == None:
                                saldoAnt = 0
                            else:
                                saldoAnt = saldoAnioanteriorTrabajo.monto_saldo
                            varHori = float(montoRecibido) - float(saldoAnt)
                            if(saldoAnt==0):
                                porHori = 1
                            else:
                                porHori = float(varHori) / float(saldoAnt)
                        else:
                            for saldoCuenta in SaldoDeCuentaBalace.objects.filter(idbalance=balanceActl.idBalance,year_saldo=datetime(analisisAuxiliar.year_analisis,1,1)):
                                totalNoActivo = float(totalNoActivo) + float(saldoCuenta.monto_saldo)
                            if totalNoActivo != 0:
                                porVert = float(montoRecibido) / float(totalNoActivo)
                            else:
                                porVert = 0
                            saldoAnioanteriorTrabajo = SaldoDeCuentaBalace.objects.filter(idCuenta=cuentaRecibida, year_saldo = datetime(int(analisisAuxiliar.year_analisis)-1,1,1)).first()
                            if saldoAnioanteriorTrabajo == None:
                                saldoAnt = 0
                            else:
                                saldoAnt = saldoAnioanteriorTrabajo.monto_saldo
                            varHori = float(montoRecibido) - float(saldoAnt)
                            if(saldoAnt==0):
                                porHori = 1
                            else:
                                porHori = float(varHori) / float(saldoAnt)
                        lineasDeInformeAuxiliar = LineaDeInforme.objects.filter(idAnalisis=analisisAuxiliar.idAnalisis,idCuenta=cuentaRecibida)
                        if lineasDeInformeAuxiliar.first() == None:
                            lineaDeInformeAuxiliar = LineaDeInforme(
                                idLineaInfo=ultimoIdLinea,
                                idCuenta=cuentaAuxiliarTrabajo,
                                idAnalisis=analisisAuxiliar,
                                variacion_horizontal=varHori,
                                porcentaje_horizontal=porHori,
                                porcentaje_vertical=porVert,
                            )
                        else:
                            lineaDeInformeAuxiliar = lineasDeInformeAuxiliar.first()
                            lineaDeInformeAuxiliar = LineaDeInforme(
                                idLineaInfo=lineaDeInformeAuxiliar.idLineaInfo,
                                idCuenta=lineaDeInformeAuxiliar.idCuenta,
                                idAnalisis=lineaDeInformeAuxiliar.idAnalisis,
                                variacion_horizontal=varHori,
                                porcentaje_horizontal=porHori,
                                porcentaje_vertical=porVert,
                            )
                        lineaDeInformeAuxiliar.save()
                    return mostrarMensajeSegunRol(request,mensajeSalida,idempresadmin)
                else:
                    raise Http404
        else:
            #El usuario no tiene permiso: Forbidden 403
            raise exceptions.PermissionDenied()
    else:
        #El usuario no se ha identificado o el sistema ha rechazado las credenciales: Unauthorized 401
        return render(request,'401.html',status=401)
    
def obtenerCuentas(tipoEstado,empresaid):
    cuentas = Cuenta.objects.filter(idEmpresa=empresaid)
    listadoCuentasSalida = []
    for cuenta in cuentas:
        if tipoEstado=="Balance":
            if cuenta.tipo_cuenta != 'Estado de Resultado' and cuenta.tipo_cuenta != 'Estado\xa0de\xa0Resultado':
                listadoCuentasSalida.append((cuenta.idCuenta,cuenta.codigo_cuenta,cuenta.nombre_cuenta))
        else:
            if cuenta.tipo_cuenta == 'Estado de Resultado' or cuenta.tipo_cuenta == 'Estado\xa0de\xa0Resultado':
                listadoCuentasSalida.append((cuenta.idCuenta,cuenta.codigo_cuenta,cuenta.nombre_cuenta))
    return listadoCuentasSalida
        

def obtenerEstados(tipoEstado,empresaid):
    listadoEstadoSalida=[]
    if(tipoEstado=="Balance"):
        #Todos los balance-empresa de la empresa
        relaciones=BalanceEmpresa.objects.filter(idEmpresa=empresaid)
        #Para cada uno de los objetos balance-empresa recuperados
        for relacion in relaciones:
            #obtener el balance que se trabajará de la relación
            balanceAux=relacion.idbalance
            #
            listadoEstadoSalida.append((balanceAux.idBalance,'Balance general del ' + str(balanceAux.yearEstado)))
            balanceAux=None
    else:
        relaciones=EstadoEmpresa.objects.filter(idEmpresa=empresaid)
        for relacion in relaciones:
            estadoAux=relacion.idResultado
            listadoEstadoSalida.append((estadoAux.idResultado,'Estado de Resultados del '+str(estadoAux.yearEstado)))
            estadoAux=None
    return listadoEstadoSalida
  #<!-- Template Main JS File -->
  #<script src="{% static 'assets/js/main.js' %}"></script>

