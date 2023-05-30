from rest_framework import serializers
from ubicacion import models

class ubicacionSerializable(serializers.ModelSerializer):
    paquete_id = serializers.IntegerField()
    paquete = serializers.CharField(read_only=True)
    class Meta:
        model = models.ubicacion
        fields = "__all__"