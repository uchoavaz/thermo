# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-13 23:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20180313_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systeminfo',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 3, 13, 23, 5, 25, 834663, tzinfo=utc), verbose_name='Date'),
        ),
    ]
