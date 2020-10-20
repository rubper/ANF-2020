from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

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
        return '{}'.format(self.idGiro)  + " " + self.nombreGiro
