from rest_framework import serializers
from user import models

class userSerializable(serializers.Serializer):
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
        ext.rol= 'U'
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
class repartidorSerializable(serializers.Serializer):
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
        ext.rol= 'R'
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