# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-12 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazi_meza_app', '0013_waterpointproblemtypes_problem_type_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='watersourceendpoint',
            name='number_of_households',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='watersourceendpoint',
            name='number_of_vulnerable_households',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='watersourceendpoint',
            name='water_point_functional',
            field=models.BooleanField(default=True),
        ),
    ]
