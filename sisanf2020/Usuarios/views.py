from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import User
from .forms import *

# Create your views here.

class CrearUsuario(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'Usuarios/CrearUsuario.html'
    success_url = reverse_lazy('Usuarios:AdministrarUsuarios')
    success_message = 'Usuario creado con éxito'

class ModificarUsuario(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'Usuarios/CrearUsuario.html'
    success_url = reverse_lazy('Usuarios:AdministrarUsuarios')
    success_message = 'Usuario modificado con éxito'

class AdministrarUsuarios(ListView):
    model = User
    template_name = 'Usuarios/AdministrarUsuarios.html'

    def get_queryset(self):
        return self.model.objects.filter(activo = True)

class EliminarUsuario(SuccessMessageMixin, DeleteView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('Usuarios:AdministrarUsuarios')
    def get_success_url(self):
        return reverse_lazy('Usuarios:AdministrarUsuarios')
