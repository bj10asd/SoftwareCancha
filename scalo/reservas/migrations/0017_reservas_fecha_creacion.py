# Generated by Django 4.1 on 2023-11-14 02:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0016_alter_reservas_anticipo_alter_reservas_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservas',
            name='fecha_creacion',
            field=models.DateTimeField(db_column='fecha_creacion', default=datetime.datetime(2023, 11, 13, 23, 45, 58, 689566), verbose_name='Fecha Creacion de Reserva'),
        ),
    ]