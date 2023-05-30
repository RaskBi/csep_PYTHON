from rest_framework import serializers
from paquete import models
import random
from drf_extra_fields.fields import Base64ImageField
from django.utils import timezone

class paqueteSerializable(serializers.ModelSerializer):
    repartidor_id= serializers.IntegerField()
    repartidor= serializers.CharField(read_only=True)
    user_id= serializers.IntegerField()
    user= serializers.CharField(read_only=True)
    paq_numero= serializers.IntegerField(default= random.randint(100000, 999999))
    paq_confirmacion= serializers.IntegerField(default= random.randint(100000, 999999))
    repartidor_location= serializers.URLField(read_only= True)
    class Meta:
        model = models.paquete
        fields = "__all__"
    def validate(self, data):
        ext= models.extencion.objects.get(id= data["repartidor_id"])
        if ext.rol != 'R':
            raise serializers.ValidationError("Un usuario no puede repartir el paquete")
        return data
class estadoPaqueteSerializable(serializers.Serializer):
    paq_imagen= Base64ImageField(use_url= True, max_length= None)
    paq_estado= serializers.CharField()
    def update(self, instance, validated_data):
        instance.paq_estado= validated_data.get('paq_estado', instance.paq_estado)
        instance.paq_imagen= validated_data.get('paq_imagen', instance.paq_imagen)
        instance.paq_fechaConfirmacion= timezone.now().strftime("%Y-%m-%d")
        instance.paq_horaConfirmacion= timezone.now().strftime("%H:%M:%S")
        instance.save()
        return instance