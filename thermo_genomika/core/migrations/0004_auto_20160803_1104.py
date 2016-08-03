# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 14:04
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20160729_0951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='systeminfo',
            options={'verbose_name': 'System Information', 'verbose_name_plural': 'Systems Informations'},
        ),
        migrations.AlterField(
            model_name='systeminfo',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 8, 3, 14, 4, 8, 187182, tzinfo=utc), verbose_name='Date'),
        ),
    ]