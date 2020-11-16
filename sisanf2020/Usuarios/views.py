from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.messages.views import SuccessMessageMixin
from .models import User, OpcionForm, AccesoUsuario
from .forms import *

# Create your views here.

class CrearUsuario(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'Usuarios/CrearUsuario.html'
    success_url = reverse_lazy('Usuarios:AdministrarUsuarios')
    success_message = 'Usuario creado con éxito'

    def form_valid(self, form):
        user=form.save(commit=False)
        if user.rol == 1:
            user.is_administrador=True
        else:
            if user.rol == 2:
                user.is_analista=True
            else:
                user.is_gerente=True

        return super(CrearUsuario, self).form_valid(form)

class ModificarUsuario(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UpdateUserForm
    template_name = 'Usuarios/CrearUsuario.html'
    success_url = reverse_lazy('Usuarios:AdministrarUsuarios')
    success_message = 'Usuario modificado con éxito'

    def form_valid(self, form):
        user=form.save(commit=False)
        if user.rol == 1:
            user.is_administrador=True
        else:
            if user.rol == 2:
                user.is_analista=True
            else:
                user.is_gerente=True

        return super(ModificarUsuario, self).form_valid(form)

class AdministrarUsuarios(ListView):
    model = User
    template_name = 'Usuarios/AdministrarUsuarios.html'

    def get(self, request):
        if request.user.is_authenticated:
            usactivo = request.user #obtiene el id del usuario que se ha autenticado
            op = '000' #Código de lista de usuarios
            usac=AccesoUsuario.objects.filter(idUsuario=usactivo).filter(idOpcion=op).values('idUsuario').first()
            if usac is None:
                return render(request, 'Usuarios/Error401.html')
            else:
                u=User.objects.all().only('id')
                return render(request, self.template_name, {"u" : u})
        else:
            return redirect('Login')

class EliminarUsuario(SuccessMessageMixin, DeleteView):
    model = User
    form_class = UserForm
    def get_success_url(self):
        return reverse_lazy('Usuarios:AdministrarUsuarios')

class Login(FormView):
    template_name = "Usuarios/Login.html"
    form_class = LoginForm
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwards):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwards)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#OpcionForm
class CrearOpcion(SuccessMessageMixin, CreateView):
    model = OpcionForm
    form_class = OpcionFormulario
    template_name = 'Usuarios/CrearOpcionForm.html'
    success_url = reverse_lazy('Usuarios:AdministrarOpcion')
    success_message = 'Opción de form creado con éxito'

class AdministrarOpciones(ListView):
    model = OpcionForm
    template_name = 'Usuarios/AdministrarOpcion.html'

    def get(self, request):
        if request.user.is_authenticated:
            usactivo = request.user #obtiene el id del usuario que se ha autenticado
            op = '001' #Código de lista de usuarios
            usac=AccesoUsuario.objects.filter(idUsuario=usactivo).filter(idOpcion=op).values('idUsuario').first()
            if usac is None:
                return render(request, 'Usuarios/Error401.html')
            else:
                opf=OpcionForm.objects.all().only('idOpcion')
                return render(request, self.template_name, {"opf" : opf})
        else:
            return redirect('Login')

class ModificarOpcion(SuccessMessageMixin, UpdateView):
    model = OpcionForm
    form_class = UpdateOpcionFormulario
    template_name = 'Usuarios/CrearOpcionForm.html'
    success_url = reverse_lazy('Usuarios:AdministrarOpcion')
    success_message = 'Opción de form modificado con éxito'


class CrearAcceso(SuccessMessageMixin, CreateView):
    model = AccesoUsuario
    form_class = AccesoUsuarioForm
    template_name = 'Usuarios/CrearAcceso.html'
    success_url = reverse_lazy('Usuarios:AdministrarAcceso')
    success_message = 'Acceso de usuario creado con éxito'

class ModificarAcceso(SuccessMessageMixin, UpdateView):
    model = AccesoUsuario
    form_class = AccesoUsuarioForm
    template_name = 'Usuarios/CrearAcceso.html'
    success_url = reverse_lazy('Usuarios:AdministrarAcceso')
    success_message = 'Acceso de usuario modificado con éxito'

class EliminarAcceso(DeleteView):
    model = AccesoUsuario
    form_class = AccesoUsuarioForm
    def get_success_url(self):
        return reverse_lazy('Usuarios:AdministrarAcceso')

class AdministrarAccesos(ListView):
    model = AccesoUsuario
    template_name = 'Usuarios/AdministrarAcceso.html'

    def get(self, request):
        if request.user.is_authenticated:
            usactivo = request.user #obtiene el id del usuario que se ha autenticado
            op = '002' #Código de lista de usuarios
            usac=AccesoUsuario.objects.filter(idUsuario=usactivo).filter(idOpcion=op).values('idUsuario').first()
            if usac is None:
                return render(request, 'Usuarios/Error401.html')
            else:
                accus=AccesoUsuario.objects.all().only('id')
                return render(request, self.template_name, {"accus" : accus})
        else:
            return redirect('Login')
