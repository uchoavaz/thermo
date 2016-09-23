
# -*- coding: utf-8 -*-
from .models import MailLog
from .models import Recipient
from .mail import send_mail


def warn_mail(thermo_info):
    email_log = 'Email sent with success'
    if not thermo_info.device_ip.min_temperature <= thermo_info.temperature <= thermo_info.device_ip.max_temperature:
        thermo_info.allowed_temp = False
        thermo_info.save()
        situation = u"ALARME !"
        recipient_list = Recipient.objects.filter(
            is_active=True).values_list('email', flat=True)
        if len(recipient_list) > 0:
            send_mail(
                thermo_info.capture_date,
                thermo_info.device_ip.local,
                thermo_info.temperature,
                situation,
                recipient_list)

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
