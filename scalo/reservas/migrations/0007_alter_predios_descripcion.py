# Generated by Django 4.1 on 2023-10-23 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0006_predios_link_mapa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predios',
            name='descripcion',
            field=models.CharField(blank=True, db_column='Desripcion', max_length=1000, null=True),
        ),
    ]
