# Generated by Django 3.2 on 2020-11-09 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaña', '0010_auto_20201109_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estado_campania',
            name='descripcion',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='tipo_resultado',
            name='descripcion',
            field=models.CharField(max_length=20),
        ),
    ]
