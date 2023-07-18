from CSEPcon.settings import MEDIA_ROOT
import getpass
from user.models import User

def crearUsuario():
    userName= input("Ingrese nombre de usuario: ")
    while True:
        password= getpass.getpass("Ingrese contraseña: ")
        if len(password)<8:
            print("La contraseña debe tener almenos 8 caracteres")
        else:
            repeat= getpass.getpass("Repita la contraseña: ")
            if password==repeat:
                break
            print("La contraseña no coincide")
    Nombre= input("Ingrese su nombre: ")
    Apellido= input("Ingrese su apellido: ")
    Correo= input("Ingrese su correo: ")
    instance= User()
    instance.username= userName
    instance.set_password(password)
    instance.first_name= Nombre
    instance.last_name= Apellido
    instance.email= Correo
    instance.save()
    return{
        "usuario_id":instance.pk,
        "rol":"A",
        "imagen":"user/default_user.png"
    }