from rest_framework import serializers
from user import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from utils.random import cbxModel
from django.db.models import Q

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
        ext.rol= 'R'
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
#crear admin
class adminSerializable(serializers.Serializer):
    id= serializers.IntegerField(read_only= True)
    first_name= serializers.CharField(required= True)
    last_name= serializers.CharField(required= True)
    username= serializers.CharField(required= True)
    email=serializers.EmailField(required= True)
    password= serializers.CharField(required= True, min_length= 8, write_only= True)
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
        ext.rol= 'A'
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
        if models.extencion.objects.filter(usuario__username=attrs.get("username"), rol="A").exists():
            user_ext = models.extencion.objects.get(usuario__username=attrs.get("username"), rol="A")
            if check_password(attrs.get("password"), user_ext.usuario.password):
                attrs["user_id"] = user_ext.usuario.pk
                # Crear o actualizar el token del usuario
                token, created = Token.objects.get_or_create(user=user_ext.usuario)
                attrs["token"] = token.key
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