from django.db import models

#Estados financieros

class EstadoDeResultado(models.Model):
    moneda_codigo=(
        ('USD','Dolares estadounodense'),
        ('SVC','Colón salvadoreño'),
        ('EUR','Euro'),
    )
    idResultado = models.AutoField(primary_key=True)
    fechaInicioEstado = models.DateField()
    fechaFinEstado = models.DateField()
    yearEstado = models.PositiveSmallIntegerField()
    moneda_estado = models.CharField(max_length=40)
    moneda_codigo_estado = models.CharField(choices=moneda_codigo,default ='USD',max_length=3)

class Balance(models.Model):
    moneda_codigo=(
        ('USD','Dolares estadounodense'),
        ('SVC','Colón salvadoreño'),
        ('EUR','Euro'),
    )
    idBalance = models.AutoField(primary_key=True)
    fechaInicioBalance = models.DateField()
    fechaFinBalance = models.DateField()
    yearEstado = models.PositiveSmallIntegerField()
    moneda_balance = models.CharField(max_length=40)
    moneda_codigo_balance = models.CharField(choices =moneda_codigo,default='USD',max_length=3)

