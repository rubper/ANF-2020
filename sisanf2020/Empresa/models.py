from django.db import models
from giros.models import Giro

# Create your models here.
class Empresa(models.Model):
    idEmpresa= models.AutoField(primary_key=True)
    idGiro=models.ForeignKey(Giro, on_delete= models.CASCADE,)
    rasonsocial =models.CharField(max_length= 50)
    telefono = models.CharField(max_length = 9)
    nrc= models.CharField(max_length =8)
    nit= models.CharField(max_length = 17)
    direccion= models.CharField(max_length = 100)

    