# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170425_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='exampledotcom',
            name='link',
            field=models.TextField(default='Default'),
        ),
        migrations.AddField(
            model_name='exampledotcom',
            name='posicion_relativa',
            field=models.TextField(default='Default'),
        ),
        migrations.AlterField(
            model_name='exampledotcom',
            name='description',
            field=models.TextField(default='Default'),
        ),
        migrations.AlterField(
            model_name='exampledotcom',
            name='title',
            field=models.TextField(default='Default'),
        ),
    ]
