from django.db import models
from django.contrib.auth.models import User
class extencion(models.Model):
    usuario= models.OneToOneField(User, on_delete= models.RESTRICT, unique= True)
    rol= models.CharField(max_length= 1)
    location= models.URLField(null= True, blank= True)
    imagen= models.ImageField(null=True, blank=True, upload_to="user/", default= "user/default_user.png")
    cedula_ruc = models.CharField(blank=True,max_length=13)
    class meta:
        verbose_name= "extencion"
        verbose_name_plural= "extenciones"

    def label_cbx(self):
        return f"{self.usuario.get_full_name()} ({self.cedula_ruc})"
    def __str__(self):
        return self.usuario.username