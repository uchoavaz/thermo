# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-18 12:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0003_auto_20160814_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicechecklist',
            name='check_date',
            field=models.DateField(default=datetime.datetime(2016, 8, 18, 12, 45, 46, 231915, tzinfo=utc), verbose_name='Check date'),
        ),
        migrations.AlterField(
            model_name='devicechecklist',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 8, 18, 12, 45, 46, 231646, tzinfo=utc), verbose_name='Date'),
        ),
    ]
