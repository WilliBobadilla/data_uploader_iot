# Generated by Django 2.2.10 on 2020-06-11 01:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_iot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medida',
            name='fecha',
            field=models.CharField(default=datetime.datetime(2020, 6, 11, 1, 33, 10, 649946), max_length=50),
        ),
    ]
