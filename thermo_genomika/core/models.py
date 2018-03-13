
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from catcher.models import AllowedAddress
from django.utils import timezone
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
    email_sent = models.BooleanField(verbose_name="E-mail Sent ?", default=None, blank=True, null=True)
    last_connection = models.BooleanField(verbose_name="Last Connection", default=None)
    check_date = models.DateTimeField(
        verbose_name=u'Check Date', default=timezone.now)
    allowed_address = models.OneToOneField(AllowedAddress)

    class Meta:
        verbose_name = (u'Device Status')
        verbose_name_plural = (u"Devices Status")