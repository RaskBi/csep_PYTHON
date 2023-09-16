from rest_framework import serializers
from user import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from utils.random import cbxModel, randomstr
from django.db.models import Q
from CSEPcon.settings import os,DIR,MEDIA_URL
from sendMail.controller import send_email
import base64

class imagenSerializable(serializers.Serializer):
    b64= serializers.CharField(allow_blank= True)
    ext= serializers.CharField(allow_blank= True)
    change= serializers.BooleanField()
    def validate(self, attrs):
        if attrs.get("change"):
            if attrs.get("b64") == "":
                raise serializers.ValidationError({"b64": "Es requerido"})
            if attrs.get("ext") == "":
                raise serializers.ValidationError({"ext": "Es requerido"})
        return attrs

class userSerializable(serializers.Serializer):
    id= serializers.IntegerField(read_only= True)
    first_name= serializers.CharField(required= True)
    last_name= serializers.CharField(required= True)
    username= serializers.CharField(required= True)
    email=serializers.EmailField(required= True)
    password= serializers.CharField(required= True, min_length= 8, write_only= True)
    cedula_ruc = serializers.CharField(min_length=10,max_length=13)
    def create(self, validated_data):
        instance= models.User()
        instance.first_name= validated_data.get('first_name')
        instance.last_name= validated_data.get('last_name')
        instance.username= validated_data.get('username')
        instance.email= validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.save()
        ext= models.extencion()
        ext.usuario= instance
        ext.rol= 'U'
        ext.cedula_ruc= validated_data.get('cedula_ruc')
        ext.save()
        return instance
    def validate_username(self,data):
        users= models.User.objects.filter(username=data)
        if len(users)!=0:
            raise serializers.ValidationError({"Error user":"Este nombre de usuario ya esta en uso"})
        else:
            return data
    def validate_email(self,data):
        users= models.User.objects.filter(email=data)
        if len(users)!=0:
            raise serializers.ValidationError({"Error email":"Este email ya esta en uso"})
        else:
            return data
    def validate(self, attrs):
        client=models.extencion.objects.filter(Q(cedula_ruc=attrs.get("cedula_ruc")) & ~Q(id=self.context.get("id")))
        print(client)
        if len(client)>=1:
            raise serializers.ValidationError({"cedula_ruc":["Este numero de cedula/RUC ya esta registrado"]})
        return attrs


class repartidorSerializable(serializers.Serializer):
    id= serializers.IntegerField(read_only= True)
    first_name= serializers.CharField(required= True)
    last_name= serializers.CharField(required= True)
    username= serializers.CharField(required= True)
    email=serializers.EmailField(required= True)
    password= serializers.CharField(min_length= 8, write_only= True, required= False)
    cedula_ruc = serializers.CharField(min_length=10,max_length=13)
    imagen_upload= imagenSerializable(default= {"change": False})
    rol= serializers.CharField(read_only= True)
    usuario_id= serializers.IntegerField(read_only= True)
    def validate_password(self, data):
        if self.context.get("id") == 0:
            raise serializers.ValidationError("Requerido")
        return data
    def create(self, validated_data):
        imagen= validated_data.pop("imagen_upload")
        folder= "user/"
        if not os.path.exists(f"{DIR}{MEDIA_URL}{folder}"):
            os.makedirs(f"{DIR}{MEDIA_URL}{folder}")
        if not imagen.get("change"):
            imagen= f"{folder}default_user.png"
        else:
            namefile= randomstr(8)
            while True:
                if os.path.exists(f"{DIR}{MEDIA_URL}{folder}{namefile}.{imagen.get('ext')}"):
                    namefile= randomstr(8)
                else:
                    break
            bites= base64.b64decode(imagen.get("b64"), validate=True)
            fh= open(f"{DIR}{MEDIA_URL}{folder}{namefile}.{imagen.get('ext')}", "wb")
            fh.write(bites)
            fh.close()
            imagen= f"{folder}{namefile}.{imagen.get('ext')}"
        instance= models.User()
        instance.first_name= validated_data.pop('first_name')
        instance.last_name= validated_data.pop('last_name')
        instance.username= validated_data.pop('username')
        instance.email= validated_data.pop('email')
        instance.set_password(validated_data.pop('password'))
        instance.save()
        validated_data["rol"]= "R"
        validated_data["imagen"]= imagen
        validated_data["usuario_id"]= instance.id
        ext= models.extencion(**validated_data)
        ext.save()
        return instance
    def validate_username(self,data):
        users= models.User.objects.filter(username=data)
        if len(users)!=0:
            raise serializers.ValidationError({"Error user":"Este nombre de usuario ya esta en uso"})
        else:
            return data
    def validate_email(self,data):
        users= models.User.objects.filter(email=data)
        if len(users)!=0:
            raise serializers.ValidationError({"Error email":"Este email ya esta en uso"})
        else:
            return data
    def update(self, instance, validated_data):
        instance.usuario.first_name= validated_data.pop('first_name')
        instance.usuario.last_name= validated_data.pop('last_name')
        instance.usuario.username= validated_data.pop('username')
        instance.usuario.email= validated_data.pop('email')
        instance.usuario.save()
        imagen= validated_data.pop("imagen_upload")
        folder= "user/"
        if imagen.get("change"):
            namefile= randomstr(8)
            while True:
                if os.path.exists(f"{DIR}{MEDIA_URL}{folder}{namefile}.{imagen.get('ext')}"):
                    namefile= randomstr(8)
                else:
                    break
            bites= base64.b64decode(imagen.get("b64"), validate=True)
            fh= open(f"{DIR}{MEDIA_URL}{folder}{namefile}.{imagen.get('ext')}", "wb")
            fh.write(bites)
            fh.close()
            imagen= f"{folder}{namefile}.{imagen.get('ext')}"
            if instance.imagen.name != "user/default_user.png":
                if os.path.exists(f"{DIR}{MEDIA_URL}{folder}{instance.imagen.name}"):
                    os.remove(f"{DIR}{MEDIA_URL}{folder}{instance.imagen.name}")
        else:
            imagen = instance.imagen.name
        validated_data["imagen"]= imagen
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    def validate_username(self,data):
        ext = models.extencion.objects.get(pk=self.context.get("id"))
        users= models.User.objects.filter(Q(username=data) & ~Q(id=ext.usuario_id))
        if len(users)!=0:
            raise serializers.ValidationError("Este nombre de usuario ya esta en uso")
        else:
            return data
    def validate_email(self,data):
        ext = models.extencion.objects.get(pk=self.context.get("id"))
        users= models.User.objects.filter(Q(email=data) & ~Q(id=ext.usuario_id))
        if len(users)!=0:
            raise serializers.ValidationError({"Error email":"Este email ya esta en uso"})
        else:
            return data
    def validate(self, attrs):
        client=models.extencion.objects.filter(Q(cedula_ruc=attrs.get("cedula_ruc")) & ~Q(id=self.context.get("id")))
        print(client)
        if len(client)>=1:
            raise serializers.ValidationError({"cedula_ruc":["Este numero de cedula/RUC ya esta registrado"]})
        return attrs
#crear admin
class adminSerializable(serializers.Serializer):
    id= serializers.IntegerField(read_only= True)
    first_name= serializers.CharField(required= True)
    last_name= serializers.CharField(required= True)
    username= serializers.CharField(required= True)
    email=serializers.EmailField(required= True)
    password= serializers.CharField(required= False, min_length= 8, write_only= True)
    cedula_ruc = serializers.CharField(min_length=10,max_length=10)
    imagen_upload= imagenSerializable(default= {"change": False})
    rol= serializers.CharField(read_only= True)
    usuario_id= serializers.IntegerField(read_only= True)
    
    def validate_password(self, data):
        if self.context.get("id") == 0:
            raise serializers.ValidationError("Requerido")
        return data
    def create(self, validated_data):
        imagen= validated_data.pop("imagen_upload")
        folder= "user/"
        if not os.path.exists(f"{DIR}{MEDIA_URL}{folder}"):
            os.makedirs(f"{DIR}{MEDIA_URL}{folder}")
        if not imagen.get("change"):
            imagen= f"{folder}default_user.png"
        else:
            namefile= randomstr(8)
            while True:
                if os.path.exists(f"{DIR}{MEDIA_URL}{folder}{namefile}.{imagen.get('ext')}"):
                    namefile= randomstr(8)
                else:
                    break
            bites= base64.b64decode(imagen.get("b64"), validate=True)
            fh= open(f"{DIR}{MEDIA_URL}{folder}{namefile}.{imagen.get('ext')}", "wb")
            fh.write(bites)
            fh.close()
            imagen= f"{folder}{namefile}.{imagen.get('ext')}"
        instance= models.User()
        instance.first_name= validated_data.pop('first_name')
        instance.last_name= validated_data.pop('last_name')
        instance.username= validated_data.pop('username')
        instance.email= validated_data.pop('email')
        instance.set_password(validated_data.pop('password'))
        instance.save()
        validated_data["rol"]= "A"
        validated_data["imagen"]= imagen
        validated_data["usuario_id"]= instance.id
        ext= models.extencion(**validated_data)
        ext.save()
        return instance
    def validate_username(self,data):
        users= models.User.objects.filter(username=data)
        if len(users)!=0:
            raise serializers.ValidationError({"Error user":"Este nombre de usuario ya esta en uso"})
        else:
            return data
    def validate_email(self,data):
        users= models.User.objects.filter(email=data)
        if len(users)!=0:
            raise serializers.ValidationError({"Error email":"Este email ya esta en uso"})
        else:
            return data



class repartidorLocationSerializable(serializers.Serializer):
    location= serializers.URLField()
    def update(self, instance, validated_data):
        instance.location= validated_data.get('location', instance.location)
        instance.save()
        return instance
class loginWebSerializable(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    imagen = serializers.ImageField(read_only=True)

    def validate(self, attrs):
        if models.extencion.objects.filter(usuario__username=attrs.get("username"), rol="A", usuario__is_active=True).exists():
            user_ext = models.extencion.objects.get(usuario__username=attrs.get("username"), rol="A")
            if check_password(attrs.get("password"), user_ext.usuario.password):
                attrs["user_id"] = user_ext.usuario.pk
                # Crear o actualizar el token del usuario
                token= Token.objects.get_or_create(user=user_ext.usuario)
                attrs["token"] = token[0]
            else:
                raise serializers.ValidationError({"detail": "Credenciales incorrectas"})
        else:
            raise serializers.ValidationError({"detail": "Credenciales incorrectas"})
        return attrs

    def create(self, validated_data):
        user_ext = models.extencion.objects.get(usuario__pk=validated_data.get("user_id"))
        validated_data["first_name"] = user_ext.usuario.first_name
        validated_data["last_name"] = user_ext.usuario.last_name
        validated_data["email"] = user_ext.usuario.email
        validated_data["imagen"] = user_ext.imagen
        return validated_data
    
class changePassword(serializers.Serializer):
    new_password = serializers.CharField(min_length=8,max_length=16)
    confirm_password = serializers.CharField(min_length=8,max_length=16)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("confirm_password"):
            raise serializers.ValidationError({"confirm_password":"Las contraseñas no coinciden"})
        return attrs
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.get("new_password"))
        instance.save()
        return instance
    
class correoChangePassword(serializers.Serializer):
    correo= serializers.EmailField()

    def validate_correo(self, data):
        print(data)
        if not models.extencion.objects.filter(usuario__email=data, rol="A", usuario__is_active=True).exists():
            raise serializers.ValidationError("Este correo no esta registrado")
        return data

    def create(self, validated_data):
        print(validated_data)
        user = models.User.objects.get(email=validated_data.get("correo"))
        send_email(user, [user.email], "Cambio de contraseña CSEP Delibery")
        return validated_data
        

    
'''   
class loginWebSerializable(serializers.Serializer):
    username= serializers.CharField()
    password= serializers.CharField(write_only=True)
    token= serializers.CharField(read_only=True)
    user_id= serializers.IntegerField(read_only=True)
    first_name=serializers.CharField(read_only=True)
    last_name=serializers.CharField(read_only=True)
    email=serializers.EmailField(read_only=True)
    imagen=serializers.ImageField(read_only=True)

    def validate(self, attrs):
        if models.extencion.objects.filter(usuario__username=attrs.get("username"), rol="A").exists():
            user_ext= models.extencion.objects.get(usuario__username=attrs.get("username"), rol="A")
            if check_password(attrs.get("password"), user_ext.usuario.password):
                attrs["user_id"]= user_ext.usuario.pk
            else:
                raise serializers.ValidationError({"detall":"Credenciales incorrectas"})
        else:
            raise serializers.ValidationError({"detall":"Credenciales incorrectas"})
        return attrs
    def create(self, validated_data):
        user_ext= models.extencion.objects.get(usuario__pk=validated_data.get("user_id"))
        tok= Token.objects.get_or_create(user=user_ext.usuario.pk)
        validated_data["token"]= tok[0]
        validated_data["first_name"]=user_ext.usuario.first_name
        validated_data["last_name"]=user_ext.usuario.last_name
        validated_data["email"]=user_ext.usuario.email
        validated_data["imagen"]=user_ext.imagen
        return validated_data''' 