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

    def get(self, request, *args, **kwards):
        if request.user.is_authenticated:
            usactivo = request.user #obtiene el id del usuario que se ha autenticado
            print("Prueba Acceso ******", usactivo)
            op = '004' #Código de lista de usuarios
            usac=AccesoUsuario.objects.filter(idUsuario=usactivo).filter(idOpcion=op).values('idUsuario').first()
            if usac is None:
                return render(request, 'Usuarios/Error401.html')
            else:
                empresas=Empresa.objects.all().only('idEmpresa')
                return render(request, self.template_name, {"empresas" : empresas})
        else:
            return redirect('Login')

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
    model=Cuenta
    form_class=CuentaForm
    template_name= 'Cuenta/Crear_Cuenta.html'
    success_url = reverse_lazy('Empresa:cuentas')

#def agregar_cuenta(request,empresa):
#    if request.method == 'POST':
#        form= CuentaForm(request.POST)
#        if form.is_valid():
#            form.save()
#        return redirect('Empresa:cuentas')
#    else:
#        form = CuentaForm()
#    return render(request,'Cuenta/Crear_Cuenta.html', {'form':form}) 



def mostrar_Cuenta(request,empresa):
    c = Cuenta.objects.filter(idEmpresa=empresa)
    cuenta ={'cuentas':c} 
    return render(request,'Cuenta/Administrador_Cuenta.html',cuenta)


