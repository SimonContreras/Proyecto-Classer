# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-03 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_classifieddata_classification'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClassifiedData',
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='classification',
            field=models.TextField(default='Default'),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='context',
            field=models.TextField(default='Default'),
        ),
        migrations.AddField(
            model_name='scrapeddata',
            name='tags',
            field=models.TextField(default='Default'),
        ),
    ]
