# Generated by Django 2.2.10 on 2020-06-13 03:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data_iot', '0004_auto_20200613_0321'),
    ]

    operations = [
        migrations.CreateModel(
            name='Codigo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='D1', max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='medida',
            name='ciudad',
        ),
        migrations.AddField(
            model_name='medida',
            name='latitud',
            field=models.FloatField(default=-45.54),
        ),
        migrations.AddField(
            model_name='medida',
            name='longitud',
            field=models.FloatField(default=-45.54),
        ),
        migrations.AlterField(
            model_name='medida',
            name='fecha',
            field=models.CharField(default=datetime.datetime(2020, 6, 13, 3, 50, 20, 830129), max_length=50),
        ),
        migrations.DeleteModel(
            name='Ciudad',
        ),
        migrations.AddField(
            model_name='medida',
            name='codigo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='data_iot.Codigo'),
        ),
    ]
