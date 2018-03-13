# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-03-13 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllowedAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=15, unique=True, verbose_name='IP')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is active?')),
                ('measure', models.IntegerField(choices=[(1, '\xbaC'), (2, '\xbaF'), (3, 'K')], default=1, verbose_name='Measure')),
                ('max_temperature', models.FloatField(default=20.0, verbose_name='Maximum temperature allowed')),
                ('min_temperature', models.FloatField(default=18.0, verbose_name='Minimum temperature allowed')),
                ('days_to_delete', models.IntegerField(default=30, verbose_name='Days to delete')),
                ('local', models.CharField(default='', max_length=150, unique=True, verbose_name='Local')),
                ('device_name', models.CharField(default='', max_length=20, verbose_name='Device Name')),
            ],
            options={
                'verbose_name': 'Allowed Address',
                'verbose_name_plural': 'Allowed Addresses',
            },
        ),
        migrations.CreateModel(
            name='ThermoInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperature', models.FloatField(verbose_name='Temperature')),
                ('capture_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Capture Date')),
                ('allowed_temp', models.BooleanField(default=True, verbose_name='Allowed Temperature ?')),
                ('device_ip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thermo_info', to='catcher.AllowedAddress', verbose_name='Device')),
            ],
            options={
                'verbose_name': 'Thermo Info',
                'verbose_name_plural': "Thermo Info's",
            },
        ),
        migrations.CreateModel(
            name='ThermoLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.TextField(verbose_name='Request')),
                ('log', models.TextField(verbose_name='LOG')),
                ('device_ip', models.CharField(max_length=15, verbose_name='Device IP')),
                ('capture_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Capture Date')),
                ('all_worked', models.BooleanField(default=False, verbose_name='All worked ?')),
            ],
            options={
                'verbose_name': 'Thermo Log',
                'verbose_name_plural': 'Thermo Logs',
            },
        ),
    ]
