from django.db import models
from Empresa.models import Empresa, Cuenta
from Giro.models import Ratios
from Estados.models import EstadoDeResultado, Balance
from datetime import datetime

# Create your models here.

def yearActual():
    return datetime.today().year

class Analisis(models.Model):
    idAnalisis = models.AutoField(primary_key=True)
    idEmpresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    year_analisis = models.PositiveSmallIntegerField(default=yearActual())
    year_previos = models.PositiveSmallIntegerField()
    estadosParaAnalisis = models.ManyToManyField(EstadoDeResultado, through='EstadoAnalisis')
    balancesParaAnalisis = models.ManyToManyField(Balance, through='BalanceAnalisis')

class LineaDeInforme(models.Model):
    idLineaInfo = models.AutoField(primary_key=True)
    idCuenta = models.ForeignKey(Cuenta,on_delete=models.CASCADE)
    idAnalisis = models.ForeignKey(Analisis,on_delete=models.CASCADE)
    variacion_horizontal = models.DecimalField(max_digits=11,decimal_places=2)
    porcentaje_horizontal = models.DecimalField(max_digits=5,decimal_places=4)
    porcentaje_vertical = models.DecimalField(max_digits=5,decimal_places=4)

class RatiosAnalisis(models.Model):
    idRatioAnalisis = models.AutoField(primary_key=True)
    idAnalisis = models.ForeignKey(Analisis,on_delete=models.CASCADE)
    idRatios = models.ForeignKey(Ratios, on_delete=models.CASCADE)
    valorRatiosAnalisis = models.DecimalField(max_digits=8,decimal_places=4)

#Muchos a muchos, clase intermedia

class EstadoAnalisis(models.Model):
    idResultado = models.ForeignKey(EstadoDeResultado, on_delete=models.CASCADE)
    idAnalisis = models.ForeignKey(Analisis, on_delete=models.CASCADE)

class BalanceAnalisis(models.Model):
    idbalance = models.ForeignKey(Balance, on_delete=models.CASCADE)
    idAnalisis = models.ForeignKey(Analisis,on_delete=models.CASCADE)