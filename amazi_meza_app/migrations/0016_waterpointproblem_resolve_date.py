# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-18 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazi_meza_app', '0015_waterpointproblem_wpp_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterpointproblem',
            name='resolve_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]