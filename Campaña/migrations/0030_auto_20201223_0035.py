# Generated by Django 3.2 on 2020-12-23 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Campaña', '0029_alter_campania_tasksids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='campania',
            old_name='dias_duracion',
            new_name='duracion',
        ),
        migrations.RenameField(
            model_name='campania',
            old_name='Fecha_Final',
            new_name='fechaFin',
        ),
        migrations.RenameField(
            model_name='campania',
            old_name='Fecha_Inicio',
            new_name='fechaInicio',
        ),
        migrations.RenameField(
            model_name='campania',
            old_name='Nombre',
            new_name='nombre',
        ),
    ]
