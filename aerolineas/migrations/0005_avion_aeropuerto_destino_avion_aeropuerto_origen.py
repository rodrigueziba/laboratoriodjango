# Generated by Django 4.2.3 on 2023-08-08 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aerolineas', '0004_customuser_avion'),
    ]

    operations = [
        migrations.AddField(
            model_name='avion',
            name='aeropuerto_destino',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='avion',
            name='aeropuerto_origen',
            field=models.CharField(max_length=100, null=True),
        ),
    ]