from rest_framework import serializers

class Consult(serializers.Serializer):
    fecha_inicio=serializers.DateField(format="%Y-%m-%d")