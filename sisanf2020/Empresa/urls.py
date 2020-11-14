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
    path('cuenta/<int:pk>',mostrar_Cuenta.as_view(),name='nueva'),
    path('cuentas',mostrar_Cuenta.as_view(),name='cuentas'),
]
