# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-26 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exocatsite', '0006_auto_20180416_1233'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imatge',
            options={'managed': True},
        ),
        migrations.AlterModelOptions(
            name='imatges',
            options={'managed': True},
        ),
        migrations.AlterField(
            model_name='imatgescitacions',
            name='fitxer',
            field=models.FileField(blank=True, null=True, upload_to='imatges_citacions_especies'),
        ),
    ]