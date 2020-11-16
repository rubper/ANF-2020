from django.urls import path
from .views import *
from . import views


app_name = 'Estados'

urlpatterns = [
    path('BalanceGeneral/e<int:empresa>/<int:anio>',views.indexBalanceGeneral, name='BalanceGeneral'),
    path('EstadoResultado/e<int:empresa>/<int:anio>',views.indexEstadoResultado, name='EstadoResultado'),
    path('',views.indexEstados, name='EstadosFinancieros'),
    path('EstadoFinancicero/e-anfadmin-<int:idempresadmin>',views.indexEstados, name='EstadosFinancieros'),
    path('confirmacion/<str:mensaje>',views.mensajeRedireccion, name='redireccionConfirmacion'),
    path('confirmacion/<int:empresaidmen>/<str:mensaje>',views.mensajeRedireccion, name='redireccionConfirmacion'),
]