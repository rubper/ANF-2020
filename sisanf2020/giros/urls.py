from django.urls import path
from .views import *


app_name = 'giros'

urlpatterns = [

    #URL para CRUD de Giros
    path('creargiro', CrearGiro.as_view(), name = 'crear_giro'),
    path('giro/<int:pk>', ModificarGiro.as_view(), name = 'modificar_giro'),
    path('giros/<int:pk>/borrar', EliminarGiro.as_view(), name = 'eliminar_giro'),
    path('giros', MostrarGiros.as_view(), name = 'administrar_giros'),
    path('creardato', CrearDato.as_view(), name = 'crear_dato'),
    path('dato/<int:pk>', ModificarDato.as_view(), name = 'modificar_dato'),
    path('datos/<int:pk>/borrar', EliminarDato.as_view(), name = 'eliminar_dato'),
    path('datos', MostrarDatos.as_view(), name = 'administrar_datos'),
]
