from django.urls import path
from .views import *
from . import views

app_name = 'Analisis'

urlpatterns = [

    #URL para  Ratios
    path('Ratios', MostrarRatios.as_view(), name = 'ListaRatios'),
    path('Importar', views.uploadRatios, name='ImportarRatios'),
    #URL analisis horizontal
    path('AnalisisHorizontal/<int:empresa>', views.indexAnalisisHorizontal, name='AnalisisHorizontal'),
    path('VerOverView/', views.VerOverView, name='VerOverView'),
    path('OverView/', views.OverView, name='OverView'),
]
