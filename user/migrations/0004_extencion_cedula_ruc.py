# Generated by Django 4.0.6 on 2023-06-27 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_extencion_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='extencion',
            name='cedula_ruc',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
