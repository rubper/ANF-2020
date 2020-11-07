from django.urls import path
from .views import *
from . import views


app_name = 'Estados'

urlpatterns = [

    path('EstadoResultado/<int:empresa>+<int:anio>',views.indexEstadoResultado, name='EstadoResultado'),
]