from django.urls import path
from .views import *
from . import views

app_name = 'ratios'

urlpatterns = [

    #URL para  Ratios
    path('ratios', MostrarRatios.as_view(), name = 'lista_ratios'),
    path('importar', views.uploadRatios, name='importar_ratios'),
]
