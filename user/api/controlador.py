from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.api import serializable
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from user.models import extencion

class userpost(APIView):
    def post(self, request):
        try:
            serial= serializable.userSerializable(data= request.data)
            if serial.is_valid():
                serial.save()
                return Response("Registrado correctamente", status= status.HTTP_201_CREATED)
            return Response(serial.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status= status.HTTP_500_INTERNAL_SERVER_ERROR)
class profile(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def get(self, request):
        try:
            for i in serializable.models.extencion.objects.filter(usuario= request.user):
                users= serializable.models.User.objects.filter(id= i.usuario_id).values("id", "username", "first_name", "last_name", "email")
                data= {
                    'id':users[0]['id'],
                    'username':users[0]['username'],
                    'first_name':users[0]['first_name'],
                    'last_name':users[0]['last_name'],
                    'email':users[0]['email'],
                    'rol':i.rol 
                }
                return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class repartidorpost(APIView):
    def post(self, request):
        try:
            serial= serializable.repartidorSerializable(data= request.data)
            if serial.is_valid():
                serial.save()
                return Response("Registrado correctamente", status= status.HTTP_201_CREATED)
            return Response(serial.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status= status.HTTP_500_INTERNAL_SERVER_ERROR)
#post admin
class adminpost(APIView):
    def post(self, request):
        try:
            serial= serializable.adminSerializable(data= request.data)
            if serial.is_valid():
                serial.save()
                return Response("Registrado correctamente", status= status.HTTP_201_CREATED)
            return Response(serial.errors, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e),status= status.HTTP_500_INTERNAL_SERVER_ERROR)

class listaRepartidor(APIView):
    #authentication_classes= [TokenAuthentication]
    #permission_classes= [IsAuthenticated]
    def get(self, request):
        try:
            repartidores= []
            url = request.META.get('wsgi.url_scheme') + '://' + request.META.get('HTTP_HOST')

            for i in serializable.models.extencion.objects.filter(rol='R').order_by("-pk"):
                users= serializable.models.User.objects.filter(id= i.usuario_id).values("id", "username", "first_name", "last_name", "email")
                data = [{
                    'id':i.id,
                    'username':users[0]['username'],
                    'first_name':users[0]['first_name'],
                    'last_name':users[0]['last_name'],
                    'email':users[0]['email'],
                    'rol':i.rol,
                    'cedula':i.cedula_ruc,
                    'imagen':f"{url}{i.imagen.url}",
                }]
                for g in data:
                    repartidores+= [g]
            return Response(repartidores,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class listaAdmin(APIView):
    #authentication_classes= [TokenAuthentication]
    #permission_classes= [IsAuthenticated]
    def get(self, request):
        try:
            repartidores= []
            url = request.META.get('wsgi.url_scheme') + '://' + request.META.get('HTTP_HOST')
            for i in serializable.models.extencion.objects.filter(rol='A').order_by("-pk"):
                users= serializable.models.User.objects.filter(id= i.usuario_id).values("id", "username", "first_name", "last_name", "email")
                data = [{
                    'id':i.id,
                    'username':users[0]['username'],
                    'first_name':users[0]['first_name'],
                    'last_name':users[0]['last_name'],
                    'email':users[0]['email'],
                    'rol':i.rol,
                    'cedula':i.cedula_ruc,
                    'imagen':f"{url}{i.imagen.url}",
                }]
                for g in data:
                    repartidores+= [g]
            return Response(repartidores,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class listaUsuario(APIView):
    #authentication_classes= [TokenAuthentication]
    #permission_classes= [IsAuthenticated]
    def get(self, request):
        try:
            usuarios= []
            url = request.META.get('wsgi.url_scheme') + '://' + request.META.get('HTTP_HOST')
            for i in serializable.models.extencion.objects.filter(rol= 'U').order_by("-pk"):
                users= serializable.models.User.objects.filter(id= i.usuario_id).values("id", "username", "first_name", "last_name", "email")
                data = [{
                    'id':users[0]['id'],
                    'username':users[0]['username'],
                    'first_name':users[0]['first_name'],
                    'last_name':users[0]['last_name'],
                    'email':users[0]['email'],
                    'rol':i.rol,
                    'cedula':i.cedula_ruc,
                    'imagen':f"{url}{i.imagen.url}",
                }]
                for g in data:
                    usuarios+= [g]
            return Response(usuarios,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class updateLocation(APIView):
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]
    def put(self, request):
        extencion= serializable.models.extencion.objects.get(usuario= request.user)
        serialize= serializable.repartidorLocationSerializable(instance= extencion, data=request.data)
        if (serialize.is_valid()):
            serialize.save()
            return Response(serialize.data, status= status.HTTP_200_OK)
        return Response(serialize.errors, status= status.HTTP_400_BAD_REQUEST)
class loginWeb(APIView):
    def post(self, request):
        try:
            serial= serializable.loginWebSerializable(data=request.data,context={"request":request})
            if serial.is_valid():
                serial.save()
                return Response(serial.data, status.HTTP_200_OK)
            return Response(serial.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e: 
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CbxUser(APIView):
    def get(self, request):
        try:
            list_cbx=[]
            for i in serializable.models.extencion.objects.filter(rol= 'U'):
                users= serializable.models.User.objects.get(id=i.usuario_id)
                data={
                    "value":users.pk,
                    "label":i.label_cbx()
                }
                list_cbx.append(data)
            return Response(list_cbx,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CbxRepartidor(APIView):
    def get(self, request):
        try:
            ext = serializable.models.extencion.objects.filter(rol= 'R')
            cbx= serializable.cbxModel(ext)
            return Response(cbx,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)