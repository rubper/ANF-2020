from django.urls import path
from .views import *


app_name = 'Empresa'

urlpatterns = [

    path('crear',crear_Empresa.as_view(), name='crear'),
    path('mostrar/<int:pk>/borrar',eliminar_Empresa.as_view(),name='eliminar'),
    path('mostrar',mostrar_Empresa.as_view(), name='mostrar'),
    path('editar/<int:pk>',editar_Empreda.as_view(),name='editar'),
    path('detalle/<int:pk>/',detalle_Empresa.as_view(),name='detalle'),
]