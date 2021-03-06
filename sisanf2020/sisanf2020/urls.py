"""sisanf2020 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from sisanf2020.views import index
from Usuarios.views import Login, Logout


urlpatterns = [
    path('', index, name="index"),
    path('admin/', admin.site.urls),
    path('Giro/', include('Giro.urls', namespace='Giro')),
    path('Empresa/', include('Empresa.urls', namespace='Empresa')),
    path('Analisis/', include('Analisis.urls', namespace='Analisis')),
    path('Usuarios/', include('Usuarios.urls', namespace='Usuarios')),
    path('Estados/', include('Estados.urls', namespace='Estados')),
    path('accounts/login/', Login.as_view(), name = 'Login'),
    path('logout', login_required(Logout), name = 'Logout'),
]
