# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-13 21:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catcher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicestatus',
            name='email_sent',
            field=models.BooleanField(default=False, verbose_name='E-mail Sent?'),
        ),
    ]
