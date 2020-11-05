from django.urls import path
from .views import *
from . import views

app_name = 'Analisis'

urlpatterns = [

    #URL para  Ratios
    path('Ratios', MostrarRatios.as_view(), name = 'ListaRatios'),
    path('Importar', views.uploadRatios, name='ImportarRatios'),
]
