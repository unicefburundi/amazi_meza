# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-07-26 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazi_meza_app', '0007_numberofwatersourceendpoint_additional_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedbudgetexpenditureandannualbudget',
            name='annual_badget',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='expectedbudgetexpenditureandannualbudget',
            name='expected_annual_expenditure',
            field=models.IntegerField(null=True),
        ),
    ]