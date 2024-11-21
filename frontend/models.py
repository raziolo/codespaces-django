from django.db import models

# Create your models here.


class Venduto(models.Model):
    data = models.DateField()
    valore = models.IntegerField(default=0)

