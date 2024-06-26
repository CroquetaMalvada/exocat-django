# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-04 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exocatsite', '0003_auto_20180404_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImatgesCitacions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.FileField(blank=True, null=True, upload_to='imatges')),
            ],
            options={
                'db_table': 'imatges_citacions_especie',
                'managed': True,
            },
        ),
        migrations.RemoveField(
            model_name='citacionsespecie',
            name='imatges',
        ),
        migrations.AddField(
            model_name='imatgescitacions',
            name='id_citacio_especie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='imatges_citacio_especie', to='exocatsite.CitacionsEspecie'),
        ),
    ]
