from django.urls import path
from .views import *
from . import views


app_name = 'Estados'

urlpatterns = [

    path('EstadoResultado/e<int:empresa>/<int:anio>',views.indexEstadoResultado, name='EstadoResultado'),
    path('EstadosFinancieros/e<int:empresa>',views.indexEstados, name='EstadosFinancieros'),
]