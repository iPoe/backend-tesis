# Generated by Django 3.2 on 2020-11-28 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Campaña', '0018_auto_20201125_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='fijo',
            field=models.CharField(default=None, max_length=15),
        ),
    ]
