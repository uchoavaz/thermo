
from __future__ import unicode_literals

from django.db import models
from account.models import ThermoUser
from catcher.models import AllowedAddress
from django.utils import timezone


class DeviceChecklist(models.Model):
    date = models.DateField(verbose_name="Date", default=timezone.now())
    device = models.ForeignKey(
        AllowedAddress,
        verbose_name=u"Device",
        related_name="device")
    avg_temp = models.FloatField(verbose_name="Temperature average")
    max_temp = models.FloatField(verbose_name="Max. temperature")
    min_temp = models.FloatField(verbose_name="Min. temperature")
    date_max_temp = models.DateTimeField(verbose_name="Max. temperature date")
    date_min_temp = models.DateTimeField(verbose_name="Min. temperature date")
    responsible = models.ForeignKey(
        ThermoUser,
        verbose_name="Responsible", related_name="device_responsible",
        null=True, blank=True)
    is_checked = models.BooleanField(
        verbose_name="Is checked ?",
        default=False)
    admeasurements = models.IntegerField(
        verbose_name="Admeasurements", default=0)
    temp_not_allwd = models.IntegerField(
        verbose_name="Temperatures not allowed",
        default=0)
    check_date = models.DateField(
        verbose_name="Check date",
        null=True,
        blank=True)

    class Meta:
        verbose_name = (u'Device Checklist')
        verbose_name_plural = (u"Devices Checklists")
