from django.urls import URLPattern, path
from report.api import controlador

urlpatterns= [
    path("prueba", controlador.reportPaquetesFecha.as_view())
]