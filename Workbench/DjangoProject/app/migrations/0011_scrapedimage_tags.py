# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-06-03 20:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_scrapeddata_context'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapedimage',
            name='tags',
            field=models.TextField(default='Default'),
        ),
    ]