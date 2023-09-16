from rest_framework import serializers
from paquete import models
from drf_extra_fields.fields import Base64ImageField
from django.utils import timezone
from utils.random import randomnum, cbxModel, cbxtovalue, cbxModelObject
from datetime import datetime
from CSEPcon.settings import os,DIR,MEDIA_URL,MEDIA_ROOT
from barcode.writer import ImageWriter
import barcode
from io import BytesIO

file_folder = f'{MEDIA_ROOT}barCode'

def barcode_Code39(text):
    EAN = barcode.get_barcode_class('Code39')
    my_ean = EAN(text, writer=ImageWriter(),add_checksum=False)
    fullname = f'{text}.png'
    fp = BytesIO()
    my_ean.write(fp)
    folder_barcode=f'{file_folder}/'
    if not os.path.exists(folder_barcode):
        os.makedirs(folder_barcode)
    with open(f"{folder_barcode}{fullname}", "wb") as f:
        my_ean.write(f)
    return f"barCode/{fullname}"

class ComboBoxSerializers(serializers.Serializer):
    value= serializers.IntegerField()
    label= serializers.CharField()

class paqueteSerializableSpecial(serializers.ModelSerializer):
    repartidor_add=ComboBoxSerializers()
    repartidor_id=serializers.IntegerField(read_only=True)
    user_add=ComboBoxSerializers()
    user_id=serializers.IntegerField(read_only=True)
    paq_tip_add=ComboBoxSerializers()
    paq_tip_id=serializers.IntegerField(read_only=True)
    paq_numero= serializers.CharField(read_only=True)
    paq_confirmacion= serializers.CharField(read_only=True)
    paq_latitud=serializers.CharField()
    paq_longitud=serializers.CharField()
    paq_telefono=serializers.CharField()
    paq_direccion=serializers.CharField()
    paq_estado=serializers.CharField(default="En espera")
    user=serializers.CharField(read_only=True)
    repartidor=serializers.CharField(read_only=True)
    paq_tip=serializers.CharField(read_only=True)
    paq_barCode=serializers.CharField(read_only=True)
    class Meta:
        model = models.paquete
        fields = "__all__"
    def validate(self, data):
        hoy= datetime.now().strftime("%Y%m%d")
        print(hoy)
        random1=randomnum(3)
        paq_numero=f"PN{hoy}{random1}"
        while True:
            if models.paquete.objects.filter(paq_numero= paq_numero).exists():
                random2=randomnum(3)
                paq_numero=f"PN{hoy}{random2}"
            else:
                break
        data["paq_numero"]= paq_numero
        random2=randomnum(3)
        paq_confirmacion=f"PC{hoy}{random2}"
        while True:
            if models.paquete.objects.filter(paq_confirmacion= paq_confirmacion).exists():
                random3=randomnum(3)
                paq_confirmacion=f"PC{hoy}{random3}"
            else:
                break
        data["paq_confirmacion"]= paq_confirmacion
        ext= models.extencion.objects.get(id= data.get("repartidor_add").get("value"))
        if ext.rol == 'U':
            raise serializers.ValidationError("Un usuario no puede repartir el paquete")
        return data
    def create(self, validated_data):
        print("entro")
        validated_data["repartidor_id"]= cbxtovalue(validated_data.pop("repartidor_add"))
        validated_data["user_id"]=  cbxtovalue(validated_data.pop("user_add"))
        validated_data["paq_tip_id"]=  cbxtovalue(validated_data.pop("paq_tip_add"))
        validated_data["paq_barCode"]= barcode_Code39(validated_data.get("paq_numero"))
        instance= models.paquete(**validated_data)
        instance.save()
        return instance
    def update(self, instance, validated_data):
        validated_data["repartidor_id"]= cbxtovalue(validated_data.pop("repartidor_add"))
        validated_data["user_id"]=  cbxtovalue(validated_data.pop("user_add"))
        validated_data["paq_tip_id"]=  cbxtovalue(validated_data.pop("paq_tip_add"))
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

def user_representation(data):
    ext=models.extencion.objects.get(usuario=data.id)
    json={
                    "value":data.pk,
                    "label":ext.label_cbx()
        }
    return json

class paqueteSerializable(serializers.ModelSerializer):
    repartidor_id= serializers.IntegerField()
    repartidor= serializers.CharField(read_only=True)
    repartidor_add= ComboBoxSerializers(read_only=True)
    user_id= serializers.IntegerField()
    user= serializers.CharField(read_only=True)
    user_add= ComboBoxSerializers(read_only=True)
    paq_numero= serializers.CharField(read_only=True)
    paq_confirmacion= serializers.CharField(read_only=True)
    repartidor_location = serializers.CharField(source='repartidor.usuario.extencion.location', read_only=True)
    #repartidor_location= serializers.URLField(read_only= True)
    paq_tip= serializers.CharField(read_only=True)
    paq_tip_id= serializers.IntegerField()
    paq_tip_add = ComboBoxSerializers(read_only=True)
    full_name_user= serializers.CharField(read_only=True)
    full_name_repartidor= serializers.CharField(read_only=True)
    cedula_ruc= serializers.CharField(read_only=True)
    class Meta:
        model = models.paquete
        fields = "__all__"
    def to_representation(self, instance):
        data = super().to_representation(instance)
        time = instance.paq_horaCreacion.strftime("%H:%M:%S")
        data["paq_horaCreacion"]= time
        if not instance.paq_horaConfirmacion is None:
            time2 = instance.paq_horaConfirmacion.strftime("%H:%M:%S")
            data["paq_horaConfirmacion"]= time2
        if data.get("paq_tip") is None:
            data["paq_tip"] = ""
        if data.get("paq_tip_id") is None:
            data["paq_tip_id"] = 0
        data["paq_tip_add"]=cbxModelObject(instance.paq_tip,value= True, name= "valor_tipo")
        data["repartidor_add"]=cbxModelObject(instance.repartidor)
        data["user_add"]=user_representation(instance.user)
        data["full_name_user"]=instance.user.get_full_name()
        data["full_name_repartidor"]=instance.repartidor.usuario.get_full_name()
        user_ext= models.extencion.objects.get(usuario=instance.user)
        data["cedula_ruc"]=user_ext.cedula_ruc
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