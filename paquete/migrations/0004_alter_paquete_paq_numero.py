# Generated by Django 4.0.6 on 2022-07-28 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paquete', '0003_rename_repartiidor_paquete_repartidor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquete',
            name='paq_numero',
            field=models.IntegerField(default=338199),
        ),
    ]
