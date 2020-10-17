from django.db import models

# Create your models here.
class Giro(models.Model):
    idGiro = models.AutoField(primary_key=True)
    nombreGiro = models.CharField(max_length=100)
    sector = models.CharField(max_length=2)

    def __str__(self):
        return '{}'.format(self.idGiro)  + " " + self.nombreGiro
