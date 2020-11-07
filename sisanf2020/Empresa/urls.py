from django.urls import path
from .views import *


app_name = 'Empresa'

urlpatterns = [

    path('crear',crear_Empresa.as_view(), name='crear'),
    path('mostrar/<int:pk>/borrar',eliminar_Empresa.as_view(),name='eliminar'),
    path('mostrar',mostrar_Empresa.as_view(), name='mostrar'),
    path('editar/<int:pk>',editar_Empreda.as_view(),name='editar'),    
    path('detalle/<int:pk>/',detalle_Empresa.as_view(),name='detalle'),
    path('cuenta/',agregar_cuenta.as_view(),name='nueva'),
    path('cuentas/<int:pk>',mostrar_Cuenta.as_view(), name='cuentas'),
]