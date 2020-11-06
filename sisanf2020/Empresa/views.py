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

class agregar_cuenta(CreateView):
    models=Cuenta
    form_class=CuentaForm
    template_name='Cuenta/Administrador_Cuenta.html'
    success_url = reverse_lazy('Cuenta:mostrar')

class mostrar_Cuenta(ListView):
    models=Cuenta
    template_name='cuenta/Administrador_Cuenta.html'