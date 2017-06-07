# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-30 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170530_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassifiedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.TextField(default='Default')),
                ('topic', models.TextField(default='Default')),
                ('url', models.TextField(default='Default')),
                ('information', models.TextField(default='Default')),
                ('tags', models.TextField(default='Default')),
                ('context', models.TextField(default='Default')),
                ('code', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]