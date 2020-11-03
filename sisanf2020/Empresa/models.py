from django.db import models
from Giro.models import Giro

# Create your models here.
class Empresa(models.Model):
    idEmpresa= models.AutoField(primary_key=True)
    idGiro=models.ForeignKey(Giro, on_delete= models.CASCADE)
    rasonsocial =models.CharField(max_length= 50)
    telefono = models.CharField(max_length = 9)
    nrc= models.CharField(max_length =8)
    nit= models.CharField(max_length = 17)
    direccion= models.CharField(max_length = 100)

    def __str__(self):
     return  self.rasonsocial

class Cuenta(models.Model):
    idCuenta = models.AutoField(primary_key=True)
    idempresa = models.ForeignKey(Empresa,on_delete=models.CASCADE)
    codigo_cuenta = models.CharField(max_length=13)
    nombre_cuenta = models.CharField(max_length=100)
    tipo_cuenta = models.CharField(max_length=25)
    naturaleza_cuenta = models.CharField(max_length=12)
