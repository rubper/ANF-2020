from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, id, nomUsuario, password = None):
        if not  id:
            raise ValueError('El usuario debe tener un id')

        usuario = self.model(id = id, nomUsuario = nomUsuario)

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, id, nomUsuario, password):
        usuario = self.create_user(id = id, nomUsuario = nomUsuario, password = password)
        usuario.administrador = True
        usuario.save()
        return usuario


class User(AbstractBaseUser):
    id = models.CharField(primary_key = True, max_length = 2)
    nomUsuario = models.CharField(unique = True, max_length = 100)
    activo = models.BooleanField(default = True)
    administrador = models.BooleanField(default = False)
    objects = UserManager()

    USERNAME_FIELD = 'nomUsuario'
    REQUIRED_FIELD = 'id'

    def __str__(self):
        return  self.nomUsuario

    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.administrador
