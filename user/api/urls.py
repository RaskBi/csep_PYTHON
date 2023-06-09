from django.urls import URLPattern, path
from user.api import controlador
from rest_framework.authtoken import views as token

urlpatterns= [
    path("post/user", controlador.userpost.as_view()),
    path("post/repartidor", controlador.repartidorpost.as_view()),
    path("profile", controlador.profile.as_view()),
    path("listarepartidor", controlador.listaRepartidor.as_view()),
    path("listaUsuario", controlador.listaUsuario.as_view()),
    path("updateLocation", controlador.updateLocation.as_view()),
    path('api-token-auth', token.obtain_auth_token),
]