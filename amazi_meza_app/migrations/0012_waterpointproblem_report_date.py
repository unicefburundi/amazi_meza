# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-08-02 11:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('amazi_meza_app', '0011_waternetworkproblemtype_water_network_problem_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterpointproblem',
            name='report_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2017, 8, 2, 11, 37, 54, 881459, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
