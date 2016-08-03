
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

MEASURE_CHOICES = (
    (1, 'ºC'),
    (2, 'ºF'),
    (3, 'K')

)


class AllowedAddress(models.Model):
    ip = models.CharField(
        verbose_name="IP",
        max_length=15,
        unique=True)
    is_active = models.BooleanField(verbose_name='Is active?', default=False)
    measure = models.IntegerField(
        verbose_name="Measure", choices=MEASURE_CHOICES, default=1)
    max_temperature = models.FloatField(
        verbose_name='Maximum temperature permitted', default=20.0)
    days_to_delete = models.IntegerField(
        verbose_name='Days to delete', default=30)
    local = models.CharField(
        verbose_name="Local", max_length=150, unique=True, default='')

    class Meta:
        verbose_name = (u'Allowed Address')
        verbose_name_plural = (u"Allowed Addresses")

    def __str__(self):
        string = self._meta.get_field("ip").verbose_name.title() \
            + ":" + self.ip + ", "
        string = string + self._meta.get_field("local").verbose_name.title() \
            + ":" + self.local + ","
        string = string + self._meta.get_field(
            "max_temperature").verbose_name.title() \
            + ":" + str(self.max_temperature) \
            + " " + self.get_measure_display().encode('ascii', 'ignore')
        return string


class ThermoInfo(models.Model):
    temperature = models.FloatField(verbose_name="Temperature")
    device_ip = models.ForeignKey(
        AllowedAddress,
        verbose_name=u"Device",
        related_name="thermo_info")
    capture_date = models.DateTimeField(
        verbose_name="Capture Date", default=timezone.now)
    allowed_temp = models.BooleanField(
        verbose_name='Allowed Temperature ?', default=True)

    class Meta:
        verbose_name = (u'Thermo Info')
        verbose_name_plural = (u"Thermo Info's")

    def __str__(self):
        string = self._meta.get_field("capture_date").verbose_name.title()
        string = string + ":" + str(self.capture_date)
        string = string + "," + \
            self._meta.get_field("temperature").verbose_name.title()
        string = string + ":" + str(self.temperature)
        string = string + "," + \
            self._meta.get_field("device_ip").verbose_name.title()
        string = string + ":" + str(self.device_ip)
        return string


class ThermoLog(models.Model):
    request = models.TextField(verbose_name="Request")
    log = models.TextField(verbose_name='LOG')
    device_ip = models.CharField(
        verbose_name="Device IP", max_length=15)
    capture_date = models.DateTimeField(
        verbose_name="Capture Date", default=timezone.now)
    all_worked = models.BooleanField(
        verbose_name='All worked ?', default=False)

    class Meta:
        verbose_name = (u'Thermo Log')
        verbose_name_plural = (u"Thermo Logs")
