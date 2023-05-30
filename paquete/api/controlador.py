from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from paquete.api import serializable
from paquete.models import paquete
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class getpaquete(APIView):
    def get(self,request):
        try:
            paquete = serializable.models.paquete.objects.all()
            serializer = serializable.paqueteSerializable(paquete,many = True, context= {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class getpaqueteEspera(APIView):
    def get(self,request):
        try:
            paquete = serializable.models.paquete.objects.filter(paq_estado= "En espera")
            serializer = serializable.paqueteSerializable(paquete,many = True, context= {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class getpaqueteEntregado(APIView):
    def get(self,request):
        try:
            paquete = serializable.models.paquete.objects.filter(paq_estado= "Entregado")
            serializer = serializable.paqueteSerializable(paquete,many = True, context= {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class getpaqueteNoEntregado(APIView):
    def get(self,request):
        try:
            paquete = serializable.models.paquete.objects.filter(paq_estado= "No entregado")
            serializer = serializable.paqueteSerializable(paquete,many = True, context= {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class postpaquete(APIView):
    def post(self,request):
        try:
            serializer = serializable.paqueteSerializable(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)        
        except Exception as e:   
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
class getpaqueteCodigo(APIView):
    def get(self,request,codigo):
        try:
            paquete = serializable.models.paquete.objects.get(paq_numero= codigo)
            data= {
                'paq_direccion':paquete.paq_direccion,
                'paq_estado':paquete.paq_estado,
                'paq_numero':paquete.paq_numero,
                'user':paquete.user,
                'user_id':paquete.user.id,
                'repartidor':paquete.repartidor,
                'repartidor_id':paquete.repartidor.id,
                'paq_latitud':paquete.paq_latitud,
                'paq_longitud':paquete.paq_longitud,
                'paq_telefono':paquete.paq_telefono,
                'paq_confirmacion':paquete.paq_confirmacion,
                'paq_fechaCreacion':paquete.paq_fechaCreacion,
                'paq_horaCreacion':paquete.paq_horaCreacion,
                'paq_fechaConfirmacion':paquete.paq_fechaConfirmacion,
                'paq_horaConfirmacion':paquete.paq_horaConfirmacion,
                'paq_imagen':paquete.paq_imagen,
                "repartidor_location":paquete.repartidor.location
            }
            serializer = serializable.paqueteSerializable(data, context= {"request":request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
class putpaqueteEstado(APIView):
    def put(self,request,id):
        try:
            paquete= serializable.models.paquete.objects.get(pk= id)
            serializer= serializable.estadoPaqueteSerializable(paquete, data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("Actualizado correctamente", status= status.HTTP_200_OK)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
class putpaquete(APIView):
    def put(self,request,id):
        try:
            paquete= serializable.models.paquete.objects.get(pk= id)
            serializer= serializable.paqueteSerializable(instance= paquete,data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(paquete, status= status.HTTP_200_OK)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


class getpaqueteEsperaU(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self,request):
        try:
            paquete = serializable.models.paquete.objects.filter(paq_estado= "En espera",user= request.user)
            serializer = serializable.paqueteSerializable(paquete,many = True, context= {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class getpaqueteEntregadoU(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self,request):
        try:
            paquete = serializable.models.paquete.objects.filter(paq_estado= "Entregado",user= request.user)
            serializer = serializable.paqueteSerializable(paquete,many = True, context= {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class getpaqueteNoEntregadoU(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self,request):
        try:
            paquete = serializable.models.paquete.objects.filter(paq_estado= "No entregado",user= request.user)
            serializer = serializable.paqueteSerializable(paquete,many = True, context= {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)