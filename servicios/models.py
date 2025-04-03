from django.db import models

# Create your models here.
class Marca(models.Model):
    nombre = models.CharField(max_length=200) 


class Carro(models.Model):
    cilindraje = models.CharField(max_length=200) 
    color = models.CharField(max_length=200) 
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
