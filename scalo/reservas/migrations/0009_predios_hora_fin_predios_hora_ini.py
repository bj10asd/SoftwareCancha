# Generated by Django 4.1 on 2023-10-30 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0008_reservas_estado_alter_predios_descripcion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='predios',
            name='hora_fin',
            field=models.CharField(blank=True, db_column='hora_fin', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='predios',
            name='hora_ini',
            field=models.CharField(blank=True, db_column='hora_ini', max_length=20, null=True),
        ),
    ]