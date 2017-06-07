# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-04 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170603_2333'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(default='TrainData')),
                ('document', models.FileField(upload_to='documents/')),
                ('upload_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
