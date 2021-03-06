from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Ratios(models.Model):
    idRatio = models.PositiveIntegerField(primary_key=True)
    categoria = models.CharField(max_length=50)
    nomRatio = models.CharField(max_length=50)
    def __str__(self):
        return self.nomRatio

class Giro(models.Model):
    SECTOR = (
        ('SP', 'Sector primario'),
        ('SS', 'Sector secundario'),
        ('ST', 'Sector terciario'),
    )
    idGiro = models.PositiveIntegerField(primary_key=True, validators=[MinValueValidator(1), MaxValueValidator(99)])
    nombreGiro = models.CharField(max_length=100)
    sector = models.CharField(choices=SECTOR, max_length=2)

    def __str__(self):
        return  self.nombreGiro

class DatoGiro(models.Model):
    idDato = models.AutoField(primary_key=True)
    idGiro = models.ForeignKey(Giro, on_delete = models.CASCADE)
    idRatio = models.ForeignKey(Ratios, on_delete = models.CASCADE)
    valorParametro = models.FloatField(default=0)
    valorPromedio = models.FloatField(default=0)

    class Meta:
        unique_together = ("idGiro", "idRatio")    

    def __str__(self):
        return '{}'.format(self.idDato)  + " " + '{}'.format(self.idGiro)   + " " + '{}'.format(self.idRatio)
