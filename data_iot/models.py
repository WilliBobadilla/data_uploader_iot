from django.db import models

from django.utils import timezone
from datetime import datetime
# Create your models here.


class Token(models.Model):
  codigo_disp=models.CharField(default='0',max_length=50)
  token=models.CharField(default='0',max_length=100)
  

  def __str__(self):
    return self.codigo_disp



class Codigo(models.Model):
  nombre= models.CharField(default='D1',max_length=50)

  def __str__(self):
    return self.nombre
  


class Medida(models.Model):
  codigo = models.ForeignKey(Codigo,on_delete=models.PROTECT,null=True)
  temperatura = models.FloatField(default=25.54)
  fecha = models.CharField(default=datetime.now(),max_length=50) 
  latitud= models.FloatField(default=-45.54)
  longitud= models.FloatField(default=-45.54)


  def __str__(self):
    return str(self.temperatura) +"-----" +str(self.fecha)

    