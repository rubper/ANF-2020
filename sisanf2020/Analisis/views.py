from django.shortcuts import render
from tablib import Dataset
from .models import Ratios
from .resources import RatiosResource
from django.contrib import messages
from django.views.generic import ListView
from django.urls import reverse

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
