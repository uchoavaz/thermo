
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from catcher.models import AllowedAddress
from django.db import models


class SystemInfo(models.Model):
    brand = models.CharField(verbose_name="Brand", max_length=50)
    designed_by = models.CharField(verbose_name="Designed by", max_length=50)
    version = models.CharField(verbose_name="Version", max_length=10)
    date = models.DateField(verbose_name="Date", default=timezone.now())

    class Meta:
        verbose_name = (u'System Information')
        verbose_name_plural = (u"Systems Informations")

class DeviceStatus(models.Model):
    first_check = models.NullBooleanField(verbose_name="First Check", default=None, blank=True, null=True)
    second_check = models.NullBooleanField(verbose_name="Second Check", default=None)
    allowed_address = models.OneToOneField(AllowedAddress)

    class Meta:
        verbose_name = (u'Device Status')
        verbose_name_plural = (u"Devices Status")