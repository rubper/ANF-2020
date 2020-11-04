from django.urls import path, re_path
from .views import *


app_name = 'Usuarios'

urlpatterns = [

    #URL para CRUD de Usuarios
    path('CrearUsuario', CrearUsuario.as_view(), name = 'CrearUsuario'),
    re_path(r'^Usuario/(?P<pk>[0-9]+)', ModificarUsuario.as_view(), name = 'ModificarUsuario'),
    re_path(r'^Usuarios/(?P<pk>[0-9]+)/Borrar', EliminarUsuario.as_view(), name = 'EliminarUsuario'),
    path('Usuarios', AdministrarUsuarios.as_view(), name = 'AdministrarUsuarios'),
]
