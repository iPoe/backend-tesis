# Generated by Django 3.2 on 2020-11-07 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaña', '0005_alter_estado_campania_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campania',
            name='Fecha_Final',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='campania',
            name='Fecha_Inicio',
            field=models.DateTimeField(),
        ),
    ]
