# Generated by Django 4.1 on 2023-10-12 02:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Canchas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(db_column='Nombre', max_length=50)),
                ('foto', models.ImageField(db_column='Foto', upload_to='upload/')),
                ('precio', models.FloatField(db_column='Precio')),
                ('anticipo', models.FloatField(db_column='Anticipo')),
            ],
            options={
                'verbose_name': 'Cancha',
                'verbose_name_plural': 'Canchas',
                'db_table': 'canchas',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Deportes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(db_column='Descripcion', max_length=40)),
            ],
            options={
                'verbose_name': 'Deporte',
                'verbose_name_plural': 'Deportes',
                'db_table': 'deportes',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(db_column='Descripcion', max_length=40)),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
                'db_table': 'roles',
                'ordering': ['descripcion'],
            },
        ),
        migrations.CreateModel(
            name='UsuarioXRoles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol_id', models.ForeignKey(db_column='rol_id', on_delete=django.db.models.deletion.PROTECT, to='reservas.roles', verbose_name='Rol')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Rol usuario',
                'verbose_name_plural': 'Roles de usuarios',
                'db_table': 'usuario_roles',
                'ordering': ['user_id'],
            },
        ),
        migrations.CreateModel(
            name='Reservas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ini', models.DateTimeField(db_column='Fecha_Ini')),
                ('fecha_fin', models.DateTimeField(db_column='Fecha_Fin')),
                ('precio', models.FloatField(db_column='Precio')),
                ('anticipo', models.FloatField(db_column='Anticipo')),
                ('cancha_id', models.ForeignKey(db_column='cancha_id', on_delete=django.db.models.deletion.PROTECT, to='reservas.canchas')),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Reserva',
                'verbose_name_plural': 'Reservas',
                'db_table': 'reservas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Predios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(db_column='Nombre', max_length=50)),
                ('direccion', models.CharField(blank=True, db_column='Direccion', max_length=250, null=True)),
                ('lat', models.FloatField(blank=True, db_column='lat', null=True)),
                ('lng', models.FloatField(blank=True, db_column='lng', null=True)),
                ('user_id', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
            options={
                'verbose_name': 'Predio',
                'verbose_name_plural': 'Predios',
                'db_table': 'predios',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='canchas',
            name='deporte_id',
            field=models.ForeignKey(db_column='deporte_id', on_delete=django.db.models.deletion.PROTECT, to='reservas.deportes', verbose_name='Deporte ID'),
        ),
        migrations.AddField(
            model_name='canchas',
            name='predio_id',
            field=models.ForeignKey(db_column='predio_id', on_delete=django.db.models.deletion.PROTECT, to='reservas.predios', verbose_name='Predio ID'),
        ),
    ]
