# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-23 17:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20160829_1456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systeminfo',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 9, 23, 17, 13, 54, 956992, tzinfo=utc), verbose_name='Date'),
        ),
    ]