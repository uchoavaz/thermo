
# -*- coding: utf-8 -*-
from .models import MailLog
from .models import Recipient
from .mail import send_mail
from django.utils import timezone


def warn_mail(thermo_info):
    email_log = 'Email sent with success'
    if not thermo_info.device_ip.min_temperature <= thermo_info.temperature <= thermo_info.device_ip.max_temperature:
        thermo_info.allowed_temp = False
        thermo_info.save()
        situation = u"ALARME !"
        recipient_list = Recipient.objects.filter(
            is_active=True).values_list('email', flat=True)
        if len(recipient_list) > 0:
            date_time = timezone.get_current_timezone().normalize(
                thermo_info.capture_date)
            send_mail(
                date_time,
                thermo_info.device_ip.local,
                situation,
                recipient_list,
                thermo_info.temperature)

        else:
            email_log = "No recipients to send"
        MailLog.objects.create(
            local=thermo_info.device_ip.local,
            temperature=thermo_info.temperature,
            situation=situation,
            recipient_list=', '.join(recipient_list)
        )
    else:
        email_log = "No e-mail sent"
        return email_log

    return email_log

def device_not_connected_mail(thermo):

    date_time = timezone.now()
    situation = "Dispositivo Offline !"
    recipient_list = Recipient.objects.filter(
        is_active=True).values_list('email', flat=True)
    local = thermo.local

    send_mail(
        date_time,
        local,
        situation,
        recipient_list)