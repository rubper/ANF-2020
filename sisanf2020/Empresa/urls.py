from django.urls import path
from .views import *


app_name = 'Empresa'

urlpatterns = [

    path('crear',crear_Empresa.as_view(), name='crear'),
  
    path('mostrar',mostrar_Empresa.as_view(), name='mostrar'),
]