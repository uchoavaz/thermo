# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-03 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catcher', '0007_thermolog_ocurred_error'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thermolog',
            name='ocurred_error',
        ),
        migrations.AddField(
            model_name='thermolog',
            name='all_worked',
            field=models.BooleanField(default=False, verbose_name='All worked ?'),
        ),
    ]