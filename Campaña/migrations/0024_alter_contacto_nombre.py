# Generated by Django 3.2 on 2020-12-22 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaña', '0023_auto_20201222_0319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
    ]
