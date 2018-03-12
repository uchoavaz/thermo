
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone


from django.db import models


class MailLog(models.Model):
    local = models.CharField(verbose_name=u'Local', max_length=150, default='')
    temperature = models.FloatField(verbose_name=u'Temperature', default=20, null=True, blank=True)
    situation = models.CharField(verbose_name=u'Situation', max_length=50)
    recipient_list = models.TextField(
        verbose_name=u'Recipient list', blank=True)
    date = models.DateTimeField(
        verbose_name=u'Date', default=timezone.now)
    class Meta:
        verbose_name = (u'Mails Log')
        verbose_name_plural = (u"Mail Logs")


class Recipient(models.Model):
    email = models.EmailField(verbose_name=u"E-mail")
    is_active = models.BooleanField(verbose_name=u'Is active ?', default=False)

    class Meta:
        verbose_name = (u'Recipient')
        verbose_name_plural = (u"Recipients")
