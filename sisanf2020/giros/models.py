from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from ratios.models import Ratios

# Create your models here.

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

    def save(self, *args, **kwargs):
        self.valorParametro = round(self.valorParametro, 4)
        self.valorPromedio = round(self.valorPromedio, 4)
        super(DatoGiro, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.idDato)  + " " + '{}'.format(self.idGiro)   + " " + '{}'.format(self.idRatio)
