# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-19 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazi_meza_app', '0006_auto_20170719_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='numberofwatersourceendpoint',
            name='additional_number',
            field=models.IntegerField(null=True),
        ),
    ]
