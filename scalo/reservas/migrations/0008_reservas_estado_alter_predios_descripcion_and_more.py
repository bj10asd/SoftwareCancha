# Generated by Django 4.1 on 2023-10-29 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0007_alter_predios_descripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservas',
            name='estado',
            field=models.CharField(choices=[('Cancelado', 'Cancelado'), ('Pendiente', 'Pendiente'), ('Activo', 'Activo'), ('Si_jugo', 'Si_jugo'), ('No_jugo', 'No_jugo')], db_column='estado', default='Pendiente', max_length=20),
        ),
        migrations.AlterField(
            model_name='predios',
            name='descripcion',
            field=models.CharField(blank=True, db_column='Desripcion', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='predios',
            name='link_mapa',
            field=models.CharField(blank=True, db_column='link_mapa', max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='pagos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(blank=True, db_column='payment_id', max_length=25, null=True)),
                ('status', models.CharField(blank=True, db_column='status', max_length=15, null=True)),
                ('monto', models.FloatField(db_column='monto')),
                ('reserva_id', models.ForeignKey(db_column='reserva_id', on_delete=django.db.models.deletion.PROTECT, to='reservas.reservas')),
            ],
            options={
                'verbose_name': 'Pago',
                'verbose_name_plural': 'Pagos',
                'db_table': 'pagos',
            },
        ),
    ]
