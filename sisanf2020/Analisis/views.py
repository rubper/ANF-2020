from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from tablib import Dataset
from Giro.models import Ratios
from .resources import RatiosResource
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse
from datetime import datetime
from Analisis.models import Analisis, LineaDeInforme, RatiosAnalisis
from Giro.models import Ratios, DatoGiro, Giro
from Empresa.models import Empresa, SaldoDeCuentaBalace, SaldoDeCuentaResultado
from Usuarios.models import AccesoUsuario, User
from Estados.models import Balance, EstadoDeResultado
from django.http import Http404

#Analisis
def VerOverView(request):
    if request.user.is_authenticated:
        usactivo = request.user.id #obtiene el id del usuario que se ha autenticado
        op = '009' #Código opción análisis
        usac=AccesoUsuario.objects.filter(idUsuario=usactivo).filter(idOpcion=op).values('idUsuario').first()
        g = User.objects.filter(id=usactivo).values('rol')
        rolg=g.get()
        rolgerente = rolg.get('rol')
        if usac is None:
            return render(request, 'Usuarios/Error401.html')
        else:
            if rolgerente == 3:
                empGerente = Empresa.objects.filter(gerente=usactivo)
                if empGerente.count() != 0:
                    return render(request, 'Analisis/VerOverView.html', {})
                else:
                    return render(request, 'Analisis/SinEmpresas.html', {})
            else:
                return render(request, 'Analisis/VerOverView.html', {})
    else:
        return redirect('Login')



#Horizontal
def indexAnalisisHorizontal(request, anio, idempresadmin=None):
    if(request.method=='POST'):
        idAnalisis = request.POST.get('analisis')
        textoConclusion = request.POST.get('conclusion')
        analisisObj = Analisis.objects.get(idAnalisis=idAnalisis)
        analisisObj.conclusion_horizontal = str(textoConclusion)
        analisisObj.save()
        return procIndexAnalisis(request,anio,1,idempresadmin,"Conclusión modificada con éxito.")
    else:
        return procIndexAnalisis(request,anio,1,idempresadmin)

#Vertical
def indexAnalisisVertical(request, anio, idempresadmin=None):
    if(request.method=='POST'):
        idAnalisis = request.POST.get('analisis')
        textoConclusion = request.POST.get('conclusion')
        analisisObj = Analisis.objects.get(idAnalisis=idAnalisis)
        analisisObj.conclusion_vertical = str(textoConclusion)
        analisisObj.save()
        return procIndexAnalisis(request,anio,2,idempresadmin,"Conclusión modificada con éxito.")
    else:
        return procIndexAnalisis(request,anio,2,idempresadmin)

def procIndexAnalisis(request, anio, vh, idempresadmin=None,mensajeExito=""):
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
            esGerente= True
        else:
            empresaActual=Empresa.objects.filter(idEmpresa=idempresadmin).first()
            esGerente = False
            if(empresaActual==None):
                 raise Http404("Oops, esta página no existe.")
        empresa = empresaActual.idEmpresa
        #######OBTENCION DE ANALISIS#######
        #Obtiene analisis
        AnalisisDeEmpresa = Analisis.objects.filter(idEmpresa=empresa,year_analisis=anio).first()
        if(AnalisisDeEmpresa!=None):
            #Aca se guarda la lista que se itera en la template
            lineaDeTabla=[]
            lineaDeTablaResultados=[]
            #Obtiene detalles del analisis
            LineasDeAnalisis = LineaDeInforme.objects.filter(idAnalisis=AnalisisDeEmpresa.idAnalisis)
            #Obtienen balances y estados
            balancesAnalisis = Balance.objects.filter(analisis__year_analisis=anio)
            balanceAnalisis = None
            balanceAnioPasado = None
            for balanc in balancesAnalisis:
                if(balanc.yearEstado == anio):
                    balanceAnalisis=balanc
                if(balanc.yearEstado == (anio-1)):
                    balanceAnioPasado=balanc
            estadosAnalisis = EstadoDeResultado.objects.filter(analisis__year_analisis=anio)
            estadoAnalisis = None
            estadoAnioPasado=None
            for estad in estadosAnalisis:
                if(estad.yearEstado == anio):
                    estadoAnalisis=estad
                if(estad.yearEstado == (anio - 1)):
                    estadoAnioPasado = estad
            if(balanceAnalisis==None or estadoAnalisis==None or balanceAnioPasado==None or estadoAnioPasado==None):
                raise Http404("No se encontró lo que buscabas.")
            saldosBalanceAnioPasado = SaldoDeCuentaBalace.objects.filter(idbalance=balanceAnioPasado.idBalance)
            saldosBalanceAnalisis = SaldoDeCuentaBalace.objects.filter(idbalance=balanceAnalisis.idBalance)
            saldosEstadoAnioPasado = SaldoDeCuentaResultado.objects.filter(idResultado=estadoAnioPasado.idResultado)
            saldosEstadoAnalisis = SaldoDeCuentaResultado.objects.filter(idResultado=estadoAnalisis.idResultado)
            listadoBalances=[]
            listadoResultados=[]
            #tuplas con los (saldos pasados, saldos presentes) del presente analisis
            for saldopasbal in saldosBalanceAnioPasado:
                for saldopresbal in saldosBalanceAnalisis:
                    if(saldopasbal.idCuenta==saldopresbal.idCuenta):
                        listadoBalances.append((saldopasbal,saldopresbal))
            for saldopas in saldosEstadoAnioPasado:
                for saldopres in saldosEstadoAnalisis:
                    if(saldopas.idCuenta == saldopres.idCuenta):
                        listadoResultados.append((saldopas,saldopres))
            for tuplabalance in listadoBalances:
                for linea in LineasDeAnalisis:
                    if(tuplabalance[1].idCuenta==linea.idCuenta):
                        lineaDeTabla.append((tuplabalance[0],tuplabalance[1],linea))
            for tuplaresultado in listadoResultados:
                for linea in LineasDeAnalisis:
                    if(tuplaresultado[1].idCuenta==linea.idCuenta):
                        lineaDeTablaResultados.append((tuplaresultado[0],tuplaresultado[1],linea))
            #tuplas con (saldos pasados, saldos presentes, detalle de linea de analisis)
            #Se guardan elementos de saldo y linea de analisis en una tupla cada uno
            #en el 0 se encuentra el saldo de cuenta y en el 1 se encuentra la línea de análisis
        else:
            LineasDeAnalisis = []
            lineaDeTabla=[]
        ######OBTENCION DE ANIOS########
        #Obtiene la lista de los ultimos 30 años a partir de hoy (orden descendente)
        ListaAniosCompleta = []
        AnioHoy = datetime.today().year
        for i in range(30):
            ListaAniosCompleta.append(AnioHoy-i)
        #Obtener los anios que ya estan usados
        ListaAniosUsados = []
        for analisises in Analisis.objects.filter(idEmpresa=empresa).order_by('year_analisis'):
            if(ListaAniosUsados.count(analisises.year_analisis)<=0):
                ListaAniosUsados.append(analisises.year_analisis)
        #Obtener años que aún no tienen análisis
        ##Con cada uno de los anios usados
        for anioUsado in ListaAniosUsados:
            #Obtener la cantidad de veces que un anio usado se encuentra en la lista completa de años (30 años)
            cantidadVecesAnioUsado = ListaAniosCompleta.count(anioUsado)
            #Si esa cantidad es mayor que 0 (es decir, se encuentra más de una vez en la lista)
            if(cantidadVecesAnioUsado>0):
                #Repetir en ciclo, la cantidad de veces que se repite el dato en la lista
                for j in range(cantidadVecesAnioUsado):
                    #Eliminar los datos encontrados
                    ListaAniosCompleta.remove(anioUsado)
        #argumentos que se enviarán a la template
        argumentos = {
            'Analisis':AnalisisDeEmpresa,
            'detallesAnalisis':lineaDeTabla,
            'detallesAnalisis2':lineaDeTablaResultados,
            'listaAnios':ListaAniosCompleta,
            'empresaActual':empresa,
            'esGerente':esGerente,
            'year':anio,
            'mensaje':mensajeExito
        }
        if(vh==1):
            return render(request, 'Analisis/AnalisisHorizontal.html', argumentos)
        elif(vh==2):
            return render(request, 'Analisis/AnalisisVertical.html', argumentos)
    else:
        return render(request, 'Usuarios/Error401.html')


def OverView(request):
    if request.method == "POST":
        empresa = request.POST['empresa']
        year = request.POST['year']
    else:
        return HttpResponseRedirect(reverse_lazy('Analisis:VerAnalisis'))

    #Listado de análisis
    AnEmp = Analisis.objects.filter(idEmpresa=empresa).filter(year_analisis=year)
    if AnEmp.count() !=0:
        for con in AnEmp:
            cAV = con.conclusion_vertical
            cAH = con.conclusion_horizontal
        #Recupero la empresa con el id que se está recibiendo
        ep = Empresa.objects.filter(idEmpresa=empresa).values('idGiro', 'rasonsocial')
        giro = ep.get()
        #Recupero el idGiro de la empresa
        giroid = giro.get('idGiro')
        rasonsocial = giro.get('rasonsocial')
        #Recupero los datos de giro que corresponden al idGiro asociado a la empresa del análisis
        dato = DatoGiro.objects.filter(idGiro=giroid).only('idGiro', 'idRatio', 'valorParametro', 'valorPromedio')
        esGerente=False
        if(request.user.rol==3):
            esGerente=True
        #Obtiene razones de análisis
        Razones = []
        for ratio in AnEmp:
            Razones += RatiosAnalisis.objects.filter(idAnalisis=ratio.idAnalisis).only('idRatios', 'valorRatiosAnalisis', 'idAnalisis')
        Contexto = {
            'AnEmp': AnEmp.order_by('idAnalisis'),
            'dato': dato,
            'Razones': Razones,
            'rasonsocial': rasonsocial,
            'year': year,
            'empresa':empresa,
            'esGerente':esGerente,
            'cAH':cAH,
            'cAV':cAV
        }
        return render(request, 'Analisis/OverView.html', Contexto)
    else:
        Contexto = {
            'AnEmp': AnEmp.order_by('idAnalisis'),
        }
        return render(request, 'Analisis/SinEmpresas.html', Contexto)


def uploadRatios(request):
    if request.method == 'POST':
        if len(request.FILES)!=0:
            ratios_resource = RatiosResource()
            dataset = Dataset()
            new_ratios = request.FILES['myfile']

            if not new_ratios.name.endswith('xlsx'):
                messages.error(request,'Error: Formato incorrecto')
                return render(request, 'Analisis/importarRatios.html')

            imported_data = dataset.load(new_ratios.read(), format='xlsx')
            for data in imported_data:
                value = Ratios(
                    data[0],
                    data[1],
                    data[2],
                    )
                value.save()
            messages.info(request, 'Ha importado los ratios, exitosamente')
        else:
            messages.error(request,'Error: Aún no ha elegido un archivo')
            return render(request, 'Analisis/importarRatios.html')
    return render(request, 'Analisis/ImportarRatios.html')

class MostrarRatios(ListView):
    model = Ratios
    template_name = 'Analisis/Ratios.html'

def Analisis_razones(request,anio,idempresadmin=None):
    op='005'
    idUsuarioActual =  request.user.id
    idRolUsuarioActual = request.user.rol
    usac = AccesoUsuario.objects.filter(idUsuario=idUsuarioActual).filter(idOpcion=op).first()
    es_Gerete= False
    if(usac!= None):
        if(idRolUsuarioActual == 3):
            empresaActual = get_object_or_404(Empresa,gerente = idUsuarioActual)
            es_Gerete = True
        else:
            empresaActual= Empresa.objects.filter(isEmpresa = idempresadmin).first()
            es_Gerete= False
            if(empresaActual == None):
                raise Http404("Esta pagina no existe.")
        empresa =empresaActual.idEmpresa
        #obtengo el analisis de la empresa 
        Analisis_Empresa = Analisis.objects.filter(idEmpresa=empresa,year_analisis=anio).first()
        if Analisis_Empresa== None:
            raise Http404("no hay analisis de la empresa .")
        #se obtiene los ratios de la empresa actual 
        Analisis_Ratios = RatiosAnalisis.objects.filter(idAnalisis= Analisis_Empresa.idAnalisis) 
        # obtener los ratios con su analisis
        if Analisis_Ratios == None:
            raise Http404("No se encontro el anlisis")
        for analisis in Analisis_Ratios:
            ratios_de_los_nalisis = Ratios.objects.filter(idRatio=analisis.idRatio)
            dato_giro = DatoGiro.objects.filter(idRatio=analisis.idRatio,idGiro=empresaActual.idGiro)
                #ratio1
            if ratios_de_los_nalisis.nomRatios == "Razón circulante":
                 #agregacion de conclusion de ratio
                if analisis.conclusion == "":
                    if analisis.valorRatiosAnalisis > 1:
                        analisis.conclusion = """la razon de liquidez corriente al ser "+str(analisis.valorRatiosAnalisis)+" por tanto superior a 1,indica que la empresa maneja mas bienes que 
                        obligaciones en el corto plazo, siendo igual al valor de parametro y el promedio de mismo giro de empresa"""
                        analisis.save()
                    if analisis.valorRatiosAnalisis<1:
                        analisis.conclusion = """la razon de liquidez corriente al ser "+str(analisis.valorRatiosAnalisis)+"por tanot por ser inferir a 1 , indica que la empresa maneja mas
                        obligaciones que bienes en el corto plazo"""
                        analisis.save()
                #ratio 2
            if ratios_de_los_nalisis.nomRatios =="Prueba ácida":
                #conlcusion se gun parametros y promedio
                if analisis.conclusion == "":
                    analisis.conclusion="""Dejando fuera los inventario,siendo estos uno de los activos corriente menos liquidos,
                    la prueba acida refleja un mayor manejo de bienes y recursos liquidos que las obligaciones en el corto plazo.Sin embargo
                    la comparacion del promedio de otras empresa con los parametros de este giro"""
                    analisis.save()
            #ratio 3
            if ratios_de_los_nalisis.nomRatios =="Razón de capital de trabajo":
                if analisis.conclusion== "":
                    analisis.conclusion = """La razon de capital de trabajo regleja,en los promedios y parametros, un valor positivo 
                    lo que se traduce en la capacidad de la empresa de sostener sus obligaciones a corto plazo """
                    analisis.save()
            #ratio 4
            if ratios_de_los_nalisis.nomRatios=="Razón de efectivo":
                if analisis.conclusion =="":
                    analisis.conclusion= """se aprecia que en le periodo se un cavor menor que 1 lo que evidencia que las deudas y obligaciones son mayores que los activos mas liquidos 
                    de la empresa.para la empresa esto se traduce en una incapacidad de hacer frente a las obligaciones"""
                    analisis.save()
                #ratio 5
            if ratios_de_los_nalisis.nomRatios=="Razón de rotación de inventario":
                if analisis.conclusion =="":
                    analisis.conclusion= """la razon de inventario muestra un aumento de las veces en las que se renueva el inventario.se puede implicar que la empresa realizo mas 
                    inversiones en el inventario"""
                    analisis.save()
                #ratio6
            if ratios_de_los_nalisis.nomRatios=="Razón de días de inventario":
                if analisis.conclusion =="":
                    analisis.conclusion= """la necesidad de rebastecer el inventario frente a los datos de parametros y promedio de su Giro"""
                    analisis.save()
                #ratio7
            if ratios_de_los_nalisis.nomRatios =="Razón de rotación de cuentas por cobrar":
                if analisis.conclusion =="":
                    analisis.conclusion= """La razón de rotación de cobros exhibe un aumento en la cantidad de veces en el año que la empresa realiza los cobros de las deudas en 
                    las que han incurrido sus clientes. Esto implica un cambio en las políticas de crédito, que se han vuelto más estrictas con el 
                    fin de compensar la latente falta de activos circulantes cuando se saldan deudas con los proveedores."""
                    analisis.save()

                #ratio8
            if ratios_de_los_nalisis.nomRatios=="Razón de periodo medio de cobranza":
                if analisis.conclusion =="":
                    analisis.conclusion= """Dependiendo de medio de cobranza la empresa se vera en la necesidad de restringir mas suspoliticas
                    de credito para poseer activos liquidos en sus cuentas y pagar sus obligaciones"""
                    analisis.save()
            #ratio 9
            if ratios_de_los_nalisis.nomRatios=="Razón de rotación de cuentas por pagar":
                if analisis.conclusion =="":
                    analisis.conclusion= """dependiendo del margen con respecto a los parametros y el promedio se podria analizar que los proveedores puede ser 
                    mas exigente en sus politica o flexibles en estas"""
                    analisis.save()
            #ratio 10     
            if ratios_de_los_nalisis.nomRatios=="Razón de periodo medio de pago":
                if analisis.conclusion =="":
                    analisis.conclusion= """este valor si es menor a la de periodo medio de cobranza implicaria que la empresa tiene dificultades financieras ya que primero paga y depues
                    realiza cobros,lo contrario si el valor es mayor la empresa esria en normalidad"""
                    analisis.save()
            #ratio 11
            if ratios_de_los_nalisis.nomRatios=="Índice de rotación de activos totales":
                if analisis.conclusion =="":
                    analisis.conclusion= """La rotacion de activos mide la eficiencia con que las empresas utilizan sus activos para generar ingresos,
                    Los ingresos por ventas es el dinero que entra en la empresa a causa de las operaciones comerciales normales de la empresa y se encuentran en el estado de resultados. 
                    Los activos totales incluyen el importe medio de los activos totales en el año y la información se encuentran en el balance de una empresa"""
                    analisis.save()
            #ratio 12
            if ratios_de_los_nalisis.nomRatios=="Índice de rotación de activos fijos":
                if analisis.conclusion =="":
                    analisis.conclusion= """ Este indicador financiero mide la eficiencia que demuestra la empresa en el uso de sus activos fijos a la hora de 
                    generar ventas. De forma aplicada, mide la productividad que logras en las ventas, considerando la inversión en activo fijo"""
                    analisis.save()
            #ratio 13
            if ratios_de_los_nalisis.nomRatios=="Índice de margen bruto":
                if analisis.conclusion =="":
                    analisis.conclusion= """mide la rentabilidad de la empresa si entre mas alta la el porcentaje mas rentable puede ser"""
                    analisis.save()
            #ratio 14
            if ratios_de_los_nalisis.nomRatios=="Índice de margen operativo":
                if analisis.conclusion =="":
                    analisis.conclusion=  """Este indicador permite identificar cómo funcionan las operaciones propias de la 
                    empresa, es decir, cómo genera rendimientos sin depender de otras actividades que no sean propias de su objetivo principa"""
                    analisis.save()
               
            #ratio 15
            if ratios_de_los_nalisis.nomRatios=="Grado de endeudamiento":
                if analisis.conclusion =="":
                    analisis.conclusion=  """Este indicador permite identificar cómo funcionan las operaciones propias de la 
                    empresa, es decir, cómo genera rendimientos sin depender de otras actividades que no sean propias de su objetivo principa"""
                    analisis.save()
            #ratio 16
            if ratios_de_los_nalisis.nomRatios=="Grado de propiedad":
                if analisis.conclusion =="":
                    analisis.conclusion=  "Representa poca fuerza financiera a largo plazo puesto que los bienes de los propietarios de la empresa (el patrimonio) representa únicamente el "+str(analisis.valorRatiosAnalisis)+ "de los activos totales durante el periodo "
                    analisis.save()
            #ratio 17
            if ratios_de_los_nalisis.nomRatios=="Razón de endeudamiento patrimonial":
                if analisis.conclusion =="":
                    analisis.conclusion=  """La razón de endeudamiento patrimonial refleja que parte de los financiamentos 
                    a largo plazo de la empresa será utilizado para cancelar deudas, pues las deudas y obligaciones sobrepasan 
                    el capital social, reserva y utilidades de la empresa"""
                    analisis.save()

            #ratio 18
            if ratios_de_los_nalisis.nomRatios=="Razón de cobertura de gastos financieros":
                if analisis.conclusion =="":
                    analisis.conclusion=  """la razón de cobertura de gastos financieros refleja la capacidad de la 
                    empresa de asumir deudas en corto plazo, en vista de que las utilidades antes de los intereses e 
                    impuestos sobrepasan los gastos financieros"""
                    analisis.save()
            #ratio 19
            if ratios_de_los_nalisis.nomRatios=="Rentabilidad neta del patrimonio":
                if analisis.conclusion =="":
                    analisis.conclusion=  """entre mas sea el valor implicaria que la capacidad que tiene el dinero de capital para proporcionar rendimiento en la empresa"""
                    analisis.save()
            #ratio 20
            if ratios_de_los_nalisis.nomRatios=="Rentabilidad por acción":
                if analisis.conclusion =="":
                    analisis.conclusion=  """indica la cantidad de dinero que se recuperan de la inversión con el reparto de los dividendos"""
                    analisis.save()
               
            #ratio 21
            if ratios_de_los_nalisis.nomRatios=="Rentabilidad del activo":
                if analisis.conclusion =="":
                    analisis.conclusion=  """el valor de este ratio refleja la capacidad que tiene la empresa para generar ganancias"""
                    analisis.save()
            #ratio 22
            if ratios_de_los_nalisis.nomRatios=="Rentabilidad sobre ventas":
                if analisis.conclusion =="":
                    analisis.conclusion=  """el valor de ratios refleja la capacidad que tiene la empresa en cuantos a la rentabilidad diponiendo de las ventas"""
                    analisis.save()
            #ratio 23
            if ratios_de_los_nalisis.nomRatios=="Rentabilidad sobre inversión":
                if analisis.conclusion =="":
                    analisis.conclusion=  """indicador financiero encargado de medir la rentabilidad de una inversión, es decir, las utilidades o 
                    ganancias que se esperan obtener en una inversión."""
                    analisis.save()
            Resultado={
                'idconclusion':analisis.idRatioAnalisis,
                'categoria':ratios_de_los_nalisis.categoria,
                'nombre': ratios_de_los_nalisis.nomRatios,
                'valor': analisis.valorRatiosAnalisis,
                'conclusion': analisis.conclusion,
            }
        contexto={
            'esGerente':es_Gerete,
            'resultado':Resultado,
            'year':anio,
            'empresa': empresaActual,
        }
        return render(request,'Analisis/Razones_Financieras.html',contexto)
    else:
        return render(request, 'Usuarios/Error401.html')