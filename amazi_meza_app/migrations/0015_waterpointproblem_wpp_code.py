# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-10-12 12:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazi_meza_app', '0014_auto_20171012_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='waterpointproblem',
            name='wpp_code',
            field=models.IntegerField(default=0),
        ),
    ]