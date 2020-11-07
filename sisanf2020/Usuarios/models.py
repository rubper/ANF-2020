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
        usuario.is_administrador = True
        usuario.save()
        return usuario

class User(AbstractBaseUser):
    ROL=[
        (1, 'Administrador'),
        (2, 'Analista'),
        (3, 'Gerente'),
    ]
    id = models.CharField(primary_key = True, max_length = 2)
    nomUsuario = models.CharField(unique = True, max_length = 100)
    activo = models.BooleanField(default = True)
    rol = models.SmallIntegerField(choices = ROL, default = 1)
    is_administrador = models.BooleanField(default = False)
    is_analista = models.BooleanField(default = False)
    is_gerente = models.BooleanField(default = False)
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
        return self.is_administrador

class OpcionForm(models.Model):
    idOpcion = models.CharField(primary_key = True, max_length = 3)
    descOpcion = models.CharField(max_length = 100)
    numForm = models.PositiveIntegerField()

    class Meta:
        unique_together = ("idOpcion", "descOpcion", "numForm")

    def __str__(self):
        return  self.descOpcion

class AccesoUsuario(models.Model):
    idUsuario = models.ForeignKey(User, on_delete = models.CASCADE)
    idOpcion = models.ForeignKey(OpcionForm, on_delete = models.CASCADE)

    class Meta:
        unique_together = ("idUsuario", "idOpcion")
