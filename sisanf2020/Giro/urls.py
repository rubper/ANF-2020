from django.urls import path
from .views import *


app_name = 'Giro'

urlpatterns = [

    #URL para CRUD de Giros
    path('CrearGiro', CrearGiro.as_view(), name = 'CrearGiro'),
    path('Giro/<int:pk>', ModificarGiro.as_view(), name = 'ModificarGiro'),
    path('Giros/<int:pk>/Borrar', EliminarGiro.as_view(), name = 'EliminarGiro'),
    path('Giros', MostrarGiros.as_view(), name = 'AdministrarGiros'),
    path('CrearDato', CrearDato.as_view(), name = 'CrearDato'),
    path('Dato/<int:pk>', ModificarDato.as_view(), name = 'ModificarDato'),
    path('Datos/<int:pk>/Borrar', EliminarDato.as_view(), name = 'EliminarDato'),
    path('Datos', MostrarDatos.as_view(), name = 'AdministrarDatos'),
]
