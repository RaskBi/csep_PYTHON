from distutils.command.upload import upload
from django.db import models
from user.models import extencion,User

class tipoPaquete(models.Model):
    nombre= models.CharField(max_length= 50)
    estado= models.BooleanField(default=True)
    codigo= models.CharField(max_length= 5)
    valor= models.FloatField()
    class Meta:
        verbose_name= "tipoPaquete"
        verbose_name_plural= "tipoPaquetes"
    def label_cbx(self):
        return f"({self.codigo}) {self.nombre}"
    def __str__(self):
        return f"({self.codigo}) {self.nombre}"

class paquete(models.Model):
    paq_direccion= models.CharField(max_length= 100)
    paq_estado= models.CharField(max_length= 45)
    paq_numero= models.CharField(max_length=13)
    user= models.ForeignKey(User, on_delete= models.RESTRICT)
    repartidor= models.ForeignKey(extencion, on_delete= models.RESTRICT)
    paq_latitud= models.CharField(max_length= 100, null= True, blank= True)
    paq_longitud= models.CharField(max_length= 100, null= True, blank= True)
    paq_telefono= models.CharField(max_length= 100, null= True, blank= True)
    paq_confirmacion= models.CharField(max_length=13)
    paq_fechaCreacion= models.DateField(auto_now_add= True)
    paq_horaCreacion= models.TimeField(auto_now_add= True)
    paq_fechaConfirmacion= models.DateField(null= True, blank= True)
    paq_horaConfirmacion= models.TimeField(null= True, blank= True)
    paq_imagen= models.ImageField(upload_to= "paquete/", null= True, blank= True)
    paq_peso= models.FloatField()
    paq_tip= models.ForeignKey(tipoPaquete, on_delete= models.RESTRICT,null= True)
    paq_precio= models.FloatField()
    paq_barCode= models.ImageField(upload_to= "barCode/", null= True, blank= True)
    paq_active= models.IntegerField(default=1)
    class meta:
        verbose_name= "paquete"
        verbose_name_plural= "paquetes"
    def __str__(self):
        return str(self.paq_numero)