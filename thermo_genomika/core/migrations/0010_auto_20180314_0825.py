# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-14 11:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20180314_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systeminfo',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 3, 14, 11, 25, 21, 951619, tzinfo=utc), verbose_name='Date'),
        ),
    ]
