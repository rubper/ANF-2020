from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
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
