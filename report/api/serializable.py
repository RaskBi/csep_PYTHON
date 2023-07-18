from rest_framework import serializers
from django.utils import timezone

class ComboboxSerializable(serializers.Serializer):
    value = serializers.IntegerField()
    label = serializers.CharField()

class Consult(serializers.Serializer):
    fecha_inicio=serializers.DateField(format="%Y-%m-%d")

class Filtro(serializers.Serializer):
    fecha_inicio=serializers.DateField()
    fecha_fin=serializers.DateField(allow_null=True)
    def validate_fecha_fin(self, data):
        if data is None:
            data=timezone.now().date()
        return data
    
class FiltroChart(serializers.Serializer):
    usuario = ComboboxSerializable(allow_null=True)
    fecha_inicio=serializers.DateField(required=False, allow_null=True)
    fecha_fin=serializers.DateField(required=False, allow_null=True)
    def validate_fecha_fin(self, data):
        if data is None:
            data=timezone.now().date()
        return data

class FiltroRepartidor(serializers.Serializer):
    repartidor_add = serializers.DictField()
    def validate_repartidor_add(self, data):
        if data is None or "value" not in data:
            raise serializers.ValidationError("Falta el filtro del repartidor")
        return data

class FiltroUsuario(serializers.Serializer):
    user_add = serializers.DictField()
    def validate_user_add(self, data):
        if data is None or "value" not in data:
            raise serializers.ValidationError("Falta el filtro del usuario")
        return data