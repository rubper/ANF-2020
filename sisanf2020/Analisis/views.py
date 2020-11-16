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
        'esGerente':esGerente
    }
    return render(request, 'Analisis/OverView.html', Contexto)


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
