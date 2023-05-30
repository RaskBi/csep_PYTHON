from django.db import models
from paquete.models import paquete

class ubicacion(models.Model):
    ubi_cordenada= models.CharField(max_length= 100)
    paquete= models.ForeignKey(paquete, on_delete= models.RESTRICT)
    class meta:
        verbose_name= "ubicacion"
        verbose_name_plural= "ubicaciones"
    def __str__(self):
        return self.ubi_cordenada