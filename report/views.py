from django.shortcuts import render
from paquete.models import paquete
from django.utils import timezone
# Create your views here.

def reports(request):
    url = request.META.get('wsgi.url_scheme') + '://' + request.META.get('HTTP_HOST')
    base_media = f"{url}/media"
    info_paquete= paquete.objects.all()
    fechaCreacion= timezone.now()
    print(fechaCreacion)
    return render(request,'paquetes/paquetes.html',{"url":url,"image":f"{base_media}/empresa/logo.png","nombre_empresa":"CSEP Delivery","paquete":info_paquete, "fechaCreacion":fechaCreacion})

