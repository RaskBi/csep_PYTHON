from django.db import models
from django.contrib.auth.models import User
class extencion(models.Model):
    usuario= models.OneToOneField(User, on_delete= models.RESTRICT, unique= True)
    rol= models.CharField(max_length= 1)
    location= models.URLField(null= True, blank= True)
    class meta:
        verbose_name= "extencion"
        verbose_name_plural= "extenciones"
    def __str__(self):
        return self.usuario.username