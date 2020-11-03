from django.db import models
from Empresa.models import Empresa, Cuenta
from datetime import datetime

# Create your models here.

class Ratios(models.Model):
    idRatio = models.PositiveIntegerField(primary_key=True)
    categoria = models.CharField(max_length=50)
    nomRatio = models.CharField(max_length=50)
    def __str__(self):
        return self.nomRatio

class Analisis(models.Model):
    idAnalisis = models.AutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    year_analisis = models.PositiveSmallIntegerField(default=yearActual)
    year_previos = models.PositiveSmallIntegerField()

class LineaDeInforme(models.Model):
    idLineaInfo = models.AutoField(primary_key=True)
    idCuenta = models.ForeignKey(Cuenta,on_delete=models.CASCADE)
    idAnalisis = models.ForeignKey(Analisis,on_delete=models.CASCADE)
    variacion_horizontal = models.DecimalField(max_digits=11,decimal_places=2)
    porcentaje_horizontal = models.DecimalField(max_digits=5,decimal_places=4)
    porcentaje_vertical = models.DecimalField(max_digits=5,decimal_places=4)

def yearActual():
    return datetime.today().year