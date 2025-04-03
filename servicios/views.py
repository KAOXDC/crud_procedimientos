from django.shortcuts import render
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework import viewsets, status
from .models import Carro
from .serializers import *


####

# Servicios con Model Viewset

class CarroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all()
    serializer_class = CarroSerializer

    def get_serializer_class(self):
        """Usar un serializador diferente para crear y actualizar"""
        if self.action in ['create', 'update']:
            return CarroCreateUpdateSerializer
        return CarroSerializer

    def retrieve(self, request, pk=None):
        """Obtener un carro por ID usando un procedimiento almacenado"""
        with connection.cursor() as cursor:
            cursor.callproc('obtener_carro_por_id', [pk])
            resultado = cursor.fetchone()

        if not resultado:
            return Response({"error": "Carro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        carro = {'id': resultado[0], 'cilindraje': resultado[1], 'color': resultado[2], 'marca': resultado[3]}
        return Response(CarroSerializer(carro).data)

    def list(self, request):
        """Obtener todos los carros usando un procedimiento almacenado"""
        with connection.cursor() as cursor:
            cursor.callproc('obtener_carros')
            resultados = cursor.fetchall()

        carros = [{'id': row[0], 'cilindraje': row[1], 'color': row[2], 'marca': row[3]} for row in resultados]
        return Response(CarroSerializer(carros, many=True).data)

    def destroy(self, request, pk=None):
        """Eliminar un carro usando un procedimiento almacenado"""
        with connection.cursor() as cursor:
            cursor.callproc('eliminar_carro', [pk])

        return Response({"message": "Carro eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)


class carroViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all()
    serializer_class = carroSerializer
 
class marcaViewSet(viewsets.ModelViewSet):
    queryset = Carro.objects.all()
    serializer_class = marcaSerializer

# buscar carros por marca 
class CarrosPorMarcaView(APIView):
    def get(self, request, marca_nombre):
        with connection.cursor() as cursor:
            cursor.callproc('obtener_carros_por_marca', [marca_nombre])
            resultados = cursor.fetchall()

        carros = [{'id': row[0], 'cilindraje': row[1], 'color': row[2]} for row in resultados]

        serializer = BuscarCarroSerializer(carros, many=True)
        return Response(serializer.data)
    

class InsertarCarroView(APIView):
    def post(self, request):
        serializer = CarroCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            cilindraje = serializer.validated_data['cilindraje']
            color = serializer.validated_data['color']
            marca_id = serializer.validated_data['marca_id']

            with connection.cursor() as cursor:
                cursor.callproc('insertar_carro', [cilindraje, color, marca_id])

            return Response({"message": "Carro insertado correctamente"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


