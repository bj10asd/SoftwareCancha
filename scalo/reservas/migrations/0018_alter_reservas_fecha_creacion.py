# Generated by Django 4.1 on 2024-01-06 01:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0017_reservas_fecha_creacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservas',
            name='fecha_creacion',
            field=models.DateTimeField(db_column='fecha_creacion', default=datetime.datetime(2024, 1, 5, 22, 14, 0, 859352), verbose_name='Fecha Creacion de Reserva'),
        ),
    ]