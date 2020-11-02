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
    template_name = 'Giro/CrearGiro.html'
    success_url = reverse_lazy('Giro:AdministrarGiros')
    success_message = 'Giro creado con éxito'

class ModificarGiro(SuccessMessageMixin, UpdateView):
    model = Giro
    form_class = UpdateGiroForm
    template_name = 'Giro/CrearGiro.html'
    success_url = reverse_lazy('Giro:AdministrarGiros')
    success_message = 'Giro modificado con éxito'

class MostrarGiros(ListView):
    model = Giro
    template_name = 'Giro/AdministrarGiros.html'

class EliminarGiro(DeleteView):
    model = Giro
    form_class = GiroForm
    success_url = reverse_lazy('Giro:AdministrarGiros')
    def get_success_url(self):
        return reverse_lazy('Giro:AdministrarGiros')

class CrearDato(SuccessMessageMixin, CreateView):
    model = DatoGiro
    form_class = DatoGiroForm
    template_name = 'Giro/CrearDato.html'
    success_url = reverse_lazy('Giro:AdministrarDatos')
    success_message = 'Dato de giro creado con éxito'

class ModificarDato(SuccessMessageMixin, UpdateView):
    model = DatoGiro
    form_class = UpdateDatoGiroForm
    template_name = 'Giro/CrearDato.html'
    success_url = reverse_lazy('Giro:AdministrarDatos')
    success_message = 'Dato de giro modificado con éxito'

class EliminarDato(DeleteView):
    model = DatoGiro
    form_class = DatoGiroForm
    success_url = reverse_lazy('Giro:AdministrarDatos')
    def get_success_url(self):
        return reverse_lazy('Giro:AdministrarDatos')

class MostrarDatos(ListView):
    model = DatoGiro
    template_name = 'Giro/AdministrarDato.html'
