from django.urls import URLPattern, path
from ubicacion.api import controlador
from rest_framework.authtoken import views as token

urlpatterns= [
    path("get/ubicacion", controlador.getubicacion.as_view()),
    path("post/ubicacion", controlador.postubicacion.as_view()),
    path('api-token-auth', token.obtain_auth_token),
]