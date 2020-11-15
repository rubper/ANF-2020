from django.urls import path
from .views import *
from . import views

app_name = 'Empresa'

urlpatterns = [
    path('crear',views.crear_Empresa, name='crear'),
    path('mostrar/<int:pk>/borrar',eliminar_Empresa.as_view(),name='eliminar'),
    path('mostrar',mostrar_Empresa.as_view(), name='mostrar'),
    path('editar/<int:idEmpresa>', views.editar_Empresa,name='editar'),
    path('detalle/<int:pk>/',detalle_Empresa.as_view(),name='detalle'),
    path('cuenta/<int:empresa>',agregar_cuenta,name='nueva_cuenta'),
    path('cuentas/<int:empresa>',mostrar_Cuenta, name='cuentas'),
    path('cuentas/<int:empresa>/<int:pk>/borrar',eliminar_cuenta,name='eliminar_cuenta'),
    path('cuentas/editar/<int:pk>/<int:empresa>',editatar_cuenta,name='editar_cuenta'),
    path('cuenta/importar/<int:empresa>',agregar_cuenta_Xls,name='importar_cuenta')
]
