from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView , DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from Giros.models import *
from Giros.forms import *
from django.contrib import messages
from django import forms

# Create your views here.

#CRUD de Giro

class CrearGiro(SuccessMessageMixin, CreateView):
    model = Giro
    form_class = GiroForm
    template_name = 'Giro/CrearGiro.html'
    success_url = reverse_lazy('Giros:administrar_giro')
    success_message = 'Cuenta creada con éxito'

class ModificarGiro(UpdateView):
    model = Giro
    form_class = GiroForm
    template_name = 'Giro/CrearGiro.html'
    success_url = reverse_lazy('Giros:administrar_giro')
    success_message = 'Cuenta creada con éxito'

class MostrarGiros(ListView):
    model = Giro
    template_name = 'Giro/AdministrarGiros.html'

class EliminarGiro(DeleteView):
    model = Giro
    form_class = GiroForm
    success_url = reverse_lazy('Giros:administrar_giro')
    def get_success_url(self):
        return reverse_lazy('Giros:administrar_giro')
