# Generated by Django 4.0.6 on 2022-08-02 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paquete', '0005_paquete_paq_latitud_paquete_paq_longitud_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='paq_confirmacion',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paquete',
            name='paq_fechaConfirmacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='paquete',
            name='paq_fechaCreacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='paquete',
            name='paq_imagen',
            field=models.ImageField(default='/', upload_to='paquete/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paquete',
            name='paq_numero',
            field=models.IntegerField(),
        ),
    ]
