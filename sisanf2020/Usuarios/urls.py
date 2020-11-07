from django.urls import path, re_path
from .views import *


app_name = 'Usuarios'

urlpatterns = [

    #URL para CRUD de Usuarios
    path('CrearUsuario', CrearUsuario.as_view(), name = 'CrearUsuario'),
    re_path(r'^Usuario/(?P<pk>\d+)', ModificarUsuario.as_view(), name = 'ModificarUsuario'),
    re_path(r'^Usuarios/(?P<pk>\d+)/Borrar', EliminarUsuario.as_view(), name = 'EliminarUsuario'),
    path('Usuarios', AdministrarUsuarios.as_view(), name = 'AdministrarUsuarios'),
    path('Usuarios', AdministrarUsuarios.as_view(), name = 'AdministrarUsuarios'),
    path('CrearOpcion', CrearOpcion.as_view(), name = 'CrearOpcion'),
    re_path(r'^Opcion/(?P<pk>\d+)', ModificarOpcion.as_view(), name = 'ModificarOpcion'),
    path('Opciones', AdministrarOpciones.as_view(), name = 'AdministrarOpcion'),
    path('CrearAcceso', CrearAcceso.as_view(), name = 'CrearAcceso'),
    path('Acceso/<int:pk>', ModificarAcceso.as_view(),name='ModificarAcceso'),
    path('Accesos/<int:pk>/Borrar', EliminarAcceso.as_view(), name = 'EliminarAcceso'),
    path('Accesos', AdministrarAccesos.as_view(), name = 'AdministrarAcceso'),
]
