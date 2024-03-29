# Generated by Django 4.0.6 on 2023-05-29 22:59

from django.db import migrations, models
from user.createAdmin import crearUsuario

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_extencion_location'),
    ]
    def nuevoUsuario(apps, schema_editor):
        nuevo= crearUsuario()
        model= apps.get_model("user","extencion")
        model.objects.create(**nuevo)
    operations = [
        migrations.AddField(
            model_name='extencion',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='user/'),
        ),
        migrations.RunPython(nuevoUsuario)
    ]
