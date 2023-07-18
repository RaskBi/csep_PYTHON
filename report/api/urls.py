from django.urls import URLPattern, path
from report.api import controlador

urlpatterns= [
    path("prueba", controlador.reportPaquetesFecha.as_view()),
    path("pruebareporte", controlador.reportPaquetesFechaNoToken.as_view()),
    path("reporterangofechaconfirmacion", controlador.reportPaquetesFechaConfirmacion.as_view()),
    path("reporterepartidor", controlador.reportPaquetesRepartidor.as_view()),
    path("reporteusuario", controlador.reportPaquetesUsuario.as_view()),
    path("chartEntregadosNoEntregados", controlador.chartEntregadosNoEntregados.as_view()),
    path("charttipopaquete", controlador.chartTipoPaquete.as_view()),
    path("chartprecio", controlador.chartPrecio.as_view()),

]