from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView , DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *
from django.contrib import messages
from django import forms

# Create your views here.

#CRUD de Giro

class CrearGiro(SuccessMessageMixin, CreateView):
    model = Giro
    form_class = GiroForm
    template_name = 'giros/crear_giro.html'
    success_url = reverse_lazy('giros:administrar_giros')
    success_message = 'Giro creado con éxito'

class ModificarGiro(SuccessMessageMixin, UpdateView):
    model = Giro
    form_class = UpdateGiroForm
    template_name = 'giros/crear_giro.html'
    success_url = reverse_lazy('giros:administrar_giros')
    success_message = 'Giro modificado con éxito'

class MostrarGiros(ListView):
    model = Giro
    template_name = 'giros/administrar_giros.html'

class EliminarGiro(DeleteView):
    model = Giro
    form_class = GiroForm
    success_url = reverse_lazy('giros:administrar_giros')
    def get_success_url(self):
        return reverse_lazy('giros:administrar_giros')

class CrearDato(SuccessMessageMixin, CreateView):
    model = DatoGiro
    form_class = DatoGiroForm
    template_name = 'giros/crear_dato.html'
    success_url = reverse_lazy('giros:administrar_datos')
    success_message = 'Dato de giro creado con éxito'

class ModificarDato(SuccessMessageMixin, UpdateView):
    model = DatoGiro
    form_class = UpdateDatoGiroForm
    template_name = 'giros/crear_dato.html'
    success_url = reverse_lazy('giros:administrar_datos')
    success_message = 'Dato de giro modificado con éxito'

class EliminarDato(DeleteView):
    model = DatoGiro
    form_class = DatoGiroForm
    success_url = reverse_lazy('giros:administrar_datos')
    def get_success_url(self):
        return reverse_lazy('giros:administrar_datos')

class MostrarDatos(ListView):
    model = DatoGiro
    template_name = 'giros/administrar_dato.html'
