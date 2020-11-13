from django.shortcuts import render
from tablib import Dataset
from Giro.models import Ratios
from .resources import RatiosResource
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse
from datetime import datetime
from Analisis.models import Analisis, LineaDeInforme, RatiosAnalisis
from Giro.models import Ratios, DatoGiro, Giro
from Empresa.models import Empresa

#Analisis
def VerOverView(request):
    return render(request, 'Analisis/VerOverView.html', {})
#Horizontal
def indexAnalisisHorizontal(request, empresa):
    #Obtiene listado de análisis
    AnalisisDeEmpresa = Analisis.objects.filter(idEmpresa=empresa)
    #Obtiene detalle de elementos del listado
    LineasDeAnalisis = []
    for analisis in AnalisisDeEmpresa:
        LineasDeAnalisis += LineaDeInforme.objects.filter(idAnalisis=analisis.idAnalisis)
    #Obtiene la lista de los ultimos 30 años a partir de hoy (orden descendente)
    ListaAniosCompleta = []
    AnioHoy = datetime.today().year
    for i in range(30):
        ListaAniosCompleta.append(AnioHoy-i)
    #Obtener los anios que ya estan usados
    ListaAniosUsados = []
    for analisises in AnalisisDeEmpresa.order_by('year_analisis'):
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
        'listaAnalisis':AnalisisDeEmpresa.order_by('idAnalisis'),
        'detallesAnalisis':LineasDeAnalisis,
        'listaAnios':ListaAniosCompleta
    }
    return render(request, 'Analisis/AnalisisHorizontal.html', argumentos)

def OverView(request):
    if request.method == "POST":
        empresa = request.POST['empresa']
        year = request.POST['year']
        print(year)

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
    #Obtiene razones de análisis
    Razones = []
    for ratio in AnEmp:
        Razones += RatiosAnalisis.objects.filter(idAnalisis=ratio.idAnalisis).only('idRatios', 'valorRatiosAnalisis', 'idAnalisis')
    Contexto = {
        'AnEmp': AnEmp.order_by('idAnalisis'),
        'dato': dato,
        'Razones': Razones,
        'rasonsocial': rasonsocial,
    }
    return render(request, 'Analisis/OverView.html', Contexto)

def uploadRatios(request):
    if request.method == 'POST':
        ratios_resource = RatiosResource()
        dataset = Dataset()
        new_ratios = request.FILES['myfile']

        if not new_ratios.name.endswith('xlsx'):
            messages.error(request,'Error: Formato incorrecto')
            return render(request, 'Analisis/importar.html')

        imported_data = dataset.load(new_ratios.read(), format='xlsx')
        for data in imported_data:
            value = Ratios(
                data[0],
                data[1],
                data[2],
                )
            value.save()
        messages.info(request, 'Ha importado los ratios, exitosamente')

    return render(request, 'Analisis/ImportarRatios.html')

class MostrarRatios(ListView):
    model = Ratios
    template_name = 'Analisis/Ratios.html'
