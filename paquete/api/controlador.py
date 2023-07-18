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
            paquete = serializable.models.paquete.objects.all().order_by('-id')
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
            serializer = serializable.paqueteSerializableSpecial(data=request.data)
            if serializer.is_valid():
                g=serializer.save()
                serial2= serializable.paqueteSerializable(g)
                return Response(serial2.data, status = status.HTTP_201_CREATED)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)        
        except Exception as e:   
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)
class getpaqueteCodigo(APIView):
    def get(self, request, codigo):
        try:
            paquete = serializable.models.paquete.objects.get(paq_numero=codigo)
            serializer = serializable.paqueteSerializable(paquete, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except serializable.models.paquete.DoesNotExist:
            return Response({"error": "El paquete con el código especificado no existe."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    def get(self,request,id):
        try:
            paquete= serializable.models.paquete.objects.get(pk= id)
            serializer= serializable.paqueteSerializable(instance= paquete,context= {"request":request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,id):
        try:
            paquete= serializable.models.paquete.objects.get(pk= id)
            serializer= serializable.paqueteSerializableSpecial(instance= paquete,data= request.data)
            if serializer.is_valid():
                g=serializer.save()
                serial2=serializable.paqueteSerializable(g)
                return Response(serial2.data, status= status.HTTP_200_OK)
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

class getpaqueteEsperaR(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self,request):
        try:
            user2= serializable.models.extencion.objects.get(usuario= request.user)
            paquete = serializable.models.paquete.objects.filter(paq_estado= "En espera",repartidor = user2) #pruebale
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
        
class getpaqueteEntregadoR(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self,request):
        try:
            user2= serializable.models.extencion.objects.get(usuario= request.user)
            paquete = serializable.models.paquete.objects.filter(paq_estado= "Entregado",repartidor = user2)
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
        
class getpaqueteNoEntregadoR(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self,request):
        try:
            user2= serializable.models.extencion.objects.get(usuario= request.user)
            paquete = serializable.models.paquete.objects.filter(paq_estado= "No entregado",repartidor = user2)
            serializer = serializable.paqueteSerializable(paquete,many = True, context= {'request': request})
            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)

class cbxTipoPaquete(APIView):
    #authentication_classes= [TokenAuthentication]
    #permission_classes= [IsAuthenticated]
    def get(self,request):
        try:
            tipoPaquete = serializable.models.tipoPaquete.objects.filter(estado= True)
            cbx = serializable.cbxModel(tipoPaquete, value= True, name= "valor_tipo")
            return Response(cbx, status = status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status = status.HTTP_500_INTERNAL_SERVER_ERROR)