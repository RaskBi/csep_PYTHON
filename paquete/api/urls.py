from django.urls import URLPattern, path
from paquete.api import controlador
from rest_framework.authtoken import views as token

urlpatterns= [
    path("get/paquete", controlador.getpaquete.as_view()),
    path("post/paquete", controlador.postpaquete.as_view()),
    path("codigo/get/<codigo>", controlador.getpaqueteCodigo.as_view()),
    path("put/estado/<id>", controlador.putpaqueteEstado.as_view()),
    path("put/paquete/<id>", controlador.putpaquete.as_view()),

    path("get/listaespera", controlador.getpaqueteEspera.as_view()),
    path("get/listaentregado", controlador.getpaqueteEntregado.as_view()),
    path("get/listanoentregado", controlador.getpaqueteNoEntregado.as_view()),

    path("get/listaenesperausuario", controlador.getpaqueteEsperaU.as_view()),
    path("get/listaenesperarepartidor", controlador.getpaqueteEsperaR.as_view()),

    path("get/listaentregadousuario", controlador.getpaqueteEntregadoU.as_view()),
    path("get/listaentregadorepartidor", controlador.getpaqueteEntregadoR.as_view()),
    
    path("get/listanoentregadousuario", controlador.getpaqueteNoEntregadoU.as_view()),
    path("get/listanoentregadorepartidor", controlador.getpaqueteNoEntregadoR.as_view()),

    path("get/tipopaquete/cbx", controlador.cbxTipoPaquete.as_view()),
]