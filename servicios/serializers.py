from rest_framework import serializers
from .views import *
from .models import *

class carroSerializer (serializers.ModelSerializer):
    class Meta:
        model = Carro 
        fields = '__all__'

class marcaSerializer (serializers.ModelSerializer):
    class Meta:
        model = Marca 
        fields = '__all__'

class BuscarCarroSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    cilindraje = serializers.CharField()
    color = serializers.CharField()

# class CarroCreateSerializer(serializers.Serializer):
#     cilindraje = serializers.CharField(max_length=200)
#     color = serializers.CharField(max_length=200)
#     marca_id = serializers.IntegerField()



# Serializador con Model Serializer
class CarroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carro
        fields = ['id', 'cilindraje', 'color', 'marca']
        # fields = '__all__'

# Model serializer 
class CarroCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carro
        fields = ['cilindraje', 'color', 'marca']

    def create(self, validated_data):
        """Usamos un procedimiento almacenado para insertar un carro"""
        cilindraje = validated_data['cilindraje']
        color = validated_data['color']
        marca_id = validated_data['marca'].id

        from django.db import connection
        with connection.cursor() as cursor:
            cursor.callproc('insertar_carro', [cilindraje, color, marca_id])

        return Carro(cilindraje=cilindraje, color=color, marca_id=marca_id)

    def update(self, instance, validated_data):
        """Usamos un procedimiento almacenado para actualizar un carro"""
        instance.cilindraje = validated_data.get('cilindraje', instance.cilindraje)
        instance.color = validated_data.get('color', instance.color)
        instance.marca = validated_data.get('marca', instance.marca)

        from django.db import connection
        with connection.cursor() as cursor:
            cursor.callproc('actualizar_carro', [instance.id, instance.cilindraje, instance.color, instance.marca.id])

        return instance
