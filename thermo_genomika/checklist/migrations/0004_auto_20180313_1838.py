# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-13 21:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0003_auto_20180313_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicechecklist',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 3, 13, 21, 38, 0, 901316, tzinfo=utc), verbose_name='Date'),
        ),
    ]
