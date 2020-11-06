from django.shortcuts import render
from .models import *
from .forms import *
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic import ListView
from django import forms
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from Usuarios.models import AccesoUsuario

# Create your views here.


class crear_Empresa(SuccessMessageMixin,CreateView):
    model= Empresa
    form_class= Empresa_Forms
    template_name= 'Empresa/Crear_Empresa.html'
    success_url = reverse_lazy('Empresa:mostrar')
    Success_message = 'Empresa creada con exito'

class mostrar_Empresa(ListView):
    model=Empresa
    template_name = 'Empresa/Administrador_Empresas.html'

#    def get(self, request, *args, **kwards):
#        if request.user.is_authenticated:
#            usactivo = request.user #obtiene el id del usuario que se ha autenticado
#            op = '004' #Código de lista de empresas
#            usac=AccesoUsuario.objects.filter(idUsuario=usactivo).filter(idOpcion=op).values('idUsuario').first()
#            if usac is None:
#                return HttpResponse('Unauthorized', status=401)
#            else:
#                return render(request, self.template_name)
#        else:
#            return HttpResponse("Error: Primero debe iniciar sesión")

class editar_Empreda(UpdateView):
    model = Empresa
    form_class = Empresa_Forms
    template_name = 'Empresa/Crear_Empresa.html'
    success_url = reverse_lazy('Empresa:mostrar')
    success_message = 'Los datos han sido modifcado'

class eliminar_Empresa(DeleteView):
    model= Empresa
    form_class = Empresa_Forms
    success_url = reverse_lazy('Empresa:mostrar')
    def get_success_url(self):
        return reverse_lazy('Empresa:mostrar')

class detalle_Empresa(DetailView):
    model=Empresa
    template_name = 'Empresa/Detalle_Empresa.html'