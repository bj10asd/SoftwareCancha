# Generated by Django 4.1 on 2023-10-17 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0002_predios_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='predios',
            name='descripcion',
            field=models.EmailField(blank=True, db_column='Desripcion', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='predios',
            name='email',
            field=models.EmailField(blank=True, db_column='Email', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='predios',
            name='telefono',
            field=models.CharField(blank=True, db_column='Telefono', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='predios',
            name='direccion',
            field=models.CharField(db_column='Direccion', max_length=250),
        ),
        migrations.AlterField(
            model_name='predios',
            name='logo',
            field=models.ImageField(db_column='Foto', upload_to='upload/'),
        ),
    ]
