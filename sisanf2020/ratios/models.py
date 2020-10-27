from django.db import models

# Create your models here.

class Ratios(models.Model):
    idRatio = models.PositiveIntegerField(primary_key=True)
    categoria = models.CharField(max_length=50)
    nomRatio = models.CharField(max_length=50)
    def __str__(self):
        return self.nomRatio
