from django.db import models

#Estados financieros

class EstadoDeResultado(models.Model):
    idResultado = models.AutoField(primary_key=True)
    fechaInicioEstado = models.DateField()
    fechaFinEstado = models.DateField()
    yearEstado = models.PositiveSmallIntegerField()
    moneda_estado = models.CharField(max_length=40)
    moneda_codigo_estado = models.CharField(max_length=3)

class Balance(models.Model):
    idBalance = models.AutoField(primary_key=True)
    fechaInicioBalance = models.DateField()
    fechaFinBalance = models.DateField()
    yearEstado = models.PositiveSmallIntegerField()
    moneda_balance = models.CharField(max_length=40)
    moneda_codigo_balance = models.CharField(max_length=3)

