# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-09 15:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20160809_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='systeminfo',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 8, 9, 15, 36, 45, 277237, tzinfo=utc), verbose_name='Date'),
        ),
    ]