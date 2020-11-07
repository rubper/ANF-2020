from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView , DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django import forms
from .models import *
from .forms import *
from Usuarios.models import AccesoUsuario

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

    def get(self, request, *args, **kwards):
        if request.user.is_authenticated:
            usactivo = request.user #obtiene el id del usuario que se ha autenticado
            print("Prueba Acceso ******", usactivo)
            op = '003' #Código de lista de usuarios
            usac=AccesoUsuario.objects.filter(idUsuario=usactivo).filter(idOpcion=op).values('idUsuario').first()
            if usac is None:
                return HttpResponse('Error 401: Unauthorized', status=401)
            else:
                giros=Giro.objects.all().only('idGiro')
                return render(request, self.template_name, {"giros" : giros})
        else:
            return HttpResponse("Error: Primero debe iniciar sesión")

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
