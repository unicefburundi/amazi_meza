# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-26 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazi_meza_app', '0010_auto_20170726_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='waternetworkproblemtype',
            name='water_network_problem_code',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
    ]
