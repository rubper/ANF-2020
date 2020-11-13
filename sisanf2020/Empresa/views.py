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
from django.shortcuts import get_object_or_404
from tablib import Dataset
from .resources import CuentaResouce

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

#CRUD de Cuetas "CATALOGO DE CUENTA"

def agregar_cuenta(request,empresa):
   
    if request.method == 'POST':
        form= CuentaForm(request.POST)
        if form.is_valid():
            #carga el objeto empresa de la base
            p = Empresa.objects.get(idEmpresa=empresa)
            pk = form.data.get("idSobreNombre")
            s = SobreNombre.objects.get(idSobreNombre=pk)
            cuen = Cuenta(
                idEmpresa = p,
                idCuenta = form.data.get("idCuenta"),
                codigo_cuenta = form.data.get("codigo_cuenta"),
                nombre_cuenta = form.data.get("nombre_cuenta"),
                tipo_cuenta = form.data.get("tipo_cuenta"),
                naturaleza_cuenta = form.data.get("naturaleza_cuenta"),
                idSobreNombre = s,
            ) 
            cuen.save()
        return redirect('Empresa:cuentas',empresa)
    else:
        form = CuentaForm()
        #se envia un diccionario con el valos de la empresa para postriotmte evaluarlo
    return render(request,'Cuenta/Crear_Cuenta.html', {'form':form,'empresa':empresa}) 

#def agregar_cuenta_Xls():
#     if request.method == 'POST':
#       cuenta_Resoucer = CuentaResouce()

        


def mostrar_Cuenta(request,empresa):
    c = Cuenta.objects.filter(idEmpresa=empresa).order_by('codigo_cuenta')
    cuenta ={'cuentas':c,
             'empresa':empresa} 
    return render(request,'Cuenta/Administrador_Cuenta.html',cuenta)

def eliminar_cuenta(request,pk,empresa):
    cuenta = Cuenta.objects.get(idCuenta=pk)
    cuenta.delete()
    return redirect('Empresa:cuentas',empresa)


def editatar_cuenta(request,pk,empresa):
    cuenta = Cuenta.objects.get(idCuenta=pk)
    p = Empresa.objects.get(idEmpresa=empresa)
    if request.method =='GET':
        form = CuentaFor(instance=cuenta)
    else:
        form = CuentaFor(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
        return redirect('Empresa:cuentas',empresa)
    return render(request,'Cuenta/Editar_cuenta.html', {'form':form,'empresa':empresa}) 