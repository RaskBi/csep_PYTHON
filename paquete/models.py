from distutils.command.upload import upload
from django.db import models
from user.models import extencion,User

class paquete(models.Model):
    paq_direccion= models.CharField(max_length= 100)
    paq_estado= models.CharField(max_length= 45)
    paq_numero= models.IntegerField()
    user= models.ForeignKey(User, on_delete= models.RESTRICT)
    repartidor= models.ForeignKey(extencion, on_delete= models.RESTRICT)
    paq_latitud= models.CharField(max_length= 100, null= True, blank= True)
    paq_longitud= models.CharField(max_length= 100, null= True, blank= True)
    paq_telefono= models.CharField(max_length= 100, null= True, blank= True)
    paq_confirmacion= models.IntegerField()
    paq_fechaCreacion= models.DateField(auto_now_add= True)
    paq_horaCreacion= models.TimeField(auto_now_add= True)
    paq_fechaConfirmacion= models.DateField(null= True, blank= True)
    paq_horaConfirmacion= models.TimeField(null= True, blank= True)
    paq_imagen= models.ImageField(upload_to= "paquete/", null= True, blank= True)
    class meta:
        verbose_name= "paquete"
        verbose_name_plural= "paquetes"
    def __str__(self):
        return str(self.paq_numero)