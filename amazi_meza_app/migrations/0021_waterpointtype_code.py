# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2019-08-28 10:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazi_meza_app', '0020_watersourceendpoint_geom'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterpointtype',
            name='code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]