from django.db import models

from django.utils import timezone
from datetime import datetime
# Create your models here.
class Medida(models.Model):
  temperatura = models.FloatField(default=25.54)
  fecha = models.CharField(default=datetime.now(),max_length=50 )


  def __str__(self):
    return str(self.temperatura) +"-----" +str(self.fecha)

    