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
from django.shortcuts import get_object_or_404
from tablib import Dataset
from .resources import CuentaResouce

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
                esGerente=False
                if rolgerente == 3:
                    empresas = Empresa.objects.filter(gerente=usactivo)
                    esGerente=True
                    return render(request, self.template_name, {"empresas" : empresas,"esGerente":esGerente})
                else:
                    empresas=Empresa.objects.all().only('idEmpresa')
                    esGerente=False
                    return render(request, self.template_name, {"empresas" : empresas,"esGerente":esGerente})
        else:
            return redirect('Login')


def editar_Empresa(request, idEmpresa=None):
    idrol = request.user.rol
    if(idrol==3 and idEmpresa==None):
        empr = Empresa.objects.filter(gerente=request.user.id).first()
    else:
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rolUsuarioActual = self.request.user.rol
        esGerente=False
        if(rolUsuarioActual==3):
            esGerente=True
        context['esGerente'] = esGerente
        return context
    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            rolUsuario = self.request.user.rol
            if(len(self.kwargs)==0 and self.request.user.rol == 3):
                return Empresa.objects.filter(gerente=self.request.user.id).first()
            elif(len(self.kwargs)!=0):
                return Empresa.objects.filter(idEmpresa=self.kwargs['pk']).first()


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

def agregar_cuenta_Xls(request,empresa):
    if request.method == 'POST':
        if len(request.FILES)!=0:
            cuenta_Resoucer = CuentaResouce()
            archivo = request.FILES['subircuenta']
            if not archivo.name.endswith('xlsx'):
                messages.error(request,'Error:El formato es incorrecto debe de ser en formato .xlsx')
                return redirect('Empresa:cuentas',empresa)
            dato = Dataset()
            dato.headers = ('codigo','nombre','tipo','naturaleza','Razon')
            importado= dato.load(archivo.read(),format='xlsx')
            for cuen in importado:
                e = Empresa.objects.get(idEmpresa=empresa)
                cuenta = Cuenta(
                    idEmpresa=e,
                    codigo_cuenta =cuen[0],
                    nombre_cuenta = cuen[1],
                    tipo_cuenta = cuen[2],
                    naturaleza_cuenta = cuen[3],
                    idSobreNombre =cuen[4]
                )
                #guarda los datos hasta encontrar uno vacio de archivo subido
                if(cuenta.codigo_cuenta != None):
                    cuenta.save()
                e=None
            messages.info(request, 'Ha importado las cuentas, exitosamente')
        else:
            messages.error(request,'no a elegido un archivo')
            return redirect('Empresa:cuentas',empresa)
        return redirect('Empresa:cuentas',empresa)
    else:
        return render(request,'cuenta/importar.html',{'empresa':empresa})


def mostrar_Cuenta(request,empresaId=None):
    empresa=0
    if(request.user.rol==3):
        empresaObj=Empresa.objects.filter(gerente=request.user.id).first()
        empresa=empresaObj.idEmpresa
    else:
        empresa=empresaId        
    c = Cuenta.objects.filter(idEmpresa=empresa).order_by('codigo_cuenta')
    cuenta ={'cuentas':c,
             'empresa':empresa}
    return render(request,'Cuenta/Administrador_Cuenta.html',cuenta)

def eliminar_cuenta(request,pk,empresa):
    cuenta = Cuenta.objects.get(idCuenta=pk)
    cuenta.delete()
    messages.warning(request,'La cuenta a sido eliminada')
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
