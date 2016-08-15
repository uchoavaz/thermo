# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-14 23:41
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicechecklist',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 8, 14, 23, 41, 42, 426201, tzinfo=utc), verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='devicechecklist',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='Is checked ?'),
        ),
        migrations.AlterField(
            model_name='devicechecklist',
            name='responsible',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='device_responsible', to=settings.AUTH_USER_MODEL, verbose_name='Responsible'),
        ),
    ]
