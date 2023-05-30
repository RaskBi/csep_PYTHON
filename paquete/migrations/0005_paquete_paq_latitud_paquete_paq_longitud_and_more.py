# Generated by Django 4.0.6 on 2022-07-30 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paquete', '0004_alter_paquete_paq_numero'),
    ]

    operations = [
        migrations.AddField(
            model_name='paquete',
            name='paq_latitud',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='paquete',
            name='paq_longitud',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='paquete',
            name='paq_telefono',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paquete',
            name='paq_numero',
            field=models.IntegerField(default=643376),
        ),
    ]
