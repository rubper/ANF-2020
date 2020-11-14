from django.shortcuts import render, redirect
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
from Usuarios.models import AccesoUsuario, User

# Create your views here.


def crear_Empresa(request):
    if request.method == 'POST':
        ger = request.POST['gerente']        
        gere = User.objects.get(id=ger)
        empresa_form = Empresa_Forms(request.POST)
        if empresa_form.is_valid():
            empresa_form.save()
            return redirect('Empresa:mostrar')
    else:
        empresa_form = Empresa_Forms()
    return render(request, 'Empresa/crear_Empresa.html', {'empresa_form':empresa_form, 'gere':gere})

class mostrar_Empresa(ListView):
    model=Empresa
    template_name = 'Empresa/Administrador_Empresas.html'

    def get(self, request, *args, **kwards):
        if request.user.is_authenticated:
            usactivo = request.user.id #obtiene el id del usuario que se ha autenticado
            op = '004' #Código de lista de usuarios
            usac=AccesoUsuario.objects.filter(idUsuario=usactivo).filter(idOpcion=op).values('idUsuario').first()
            g = User.objects.filter(id=usactivo).values('rol')
            rolg=g.get()
            rolgerente = rolg.get('rol')
            print(rolgerente)
            if usac is None:
                return render(request, 'Usuarios/Error401.html')
            else:
                if rolgerente == 3:
                    empresas = Empresa.objects.filter(gerente=usactivo)
                    return render(request, self.template_name, {"empresas" : empresas})
                else:
                    empresas=Empresa.objects.all().only('idEmpresa')
                    return render(request, self.template_name, {"empresas" : empresas})
        else:
            return redirect('Login')

def editar_Empresa(request, idEmpresa):
    empr = Empresa.objects.get(idEmpresa = idEmpresa)
    if request.method == 'GET':
        empresa_form = Empresa_Forms(instance = empr)
    else:
        empresa_form = Empresa_Forms(request.POST, instance = empr)
        if empresa_form.is_valid():
            empresa_form.save()
        return redirect('Empresa:mostrar')
    return render(request, 'Empresa/crear_Empresa.html', {'empresa_form':empresa_form})


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
