# Generated by Django 2.2.10 on 2020-06-13 03:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_iot', '0003_auto_20200613_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medida',
            name='fecha',
            field=models.CharField(default=datetime.datetime(2020, 6, 13, 3, 21, 5, 226257), max_length=50),
        ),
    ]