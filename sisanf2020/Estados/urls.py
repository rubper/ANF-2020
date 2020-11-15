from django.urls import path
from .views import *
from . import views


app_name = 'Estados'

urlpatterns = [
    path('BalanceGeneral/e<int:empresa>/<int:anio>',views.indexBalanceGeneral, name='BalanceGeneral'),
    path('EstadoResultado/e<int:empresa>/<int:anio>',views.indexEstadoResultado, name='EstadoResultado'),
    path('e<int:empresa>',views.indexEstados, name='EstadosFinancieros'),
    path('confirmacion/<int:empresa>/<str:mensaje>',views.mensajeRedireccion, name='redireccionConfirmacion'),
]