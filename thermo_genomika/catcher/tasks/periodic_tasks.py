# -*- coding: utf-8 -*-

from pyping import ping
from datetime import timedelta
from django.utils import timezone
from catcher.models import DeviceStatus
from catcher.models import AllowedAddress
from celery.task.base import periodic_task
from mailer.tasks import device_not_connected_mail

def check_device_status(thermo, device_line):

    send_email = False
    message = "Dispositivo Offline !"

    devices_status = DeviceStatus.objects.filter(allowed_address__ip=thermo.ip)

    if devices_status:

        device_status = devices_status[0]

        if device_line and not device_status.last_connection:
            device_status.email_sent = False
            send_email = True
            message = "Dispositivo Online !"

        elif not device_line and device_status.last_connection and not device_status.email_sent:
            device_status.email_sent = True
            send_email = True

        device_status.last_connection = device_line
        device_status.check_date = timezone.get_current_timezone().normalize(timezone.now())

    else:

        if device_line:
            message = "Dispositivo Online !"
            send_email = True

        DeviceStatus.objects.create(
            email_sent=True,
            last_connection=device_line,
            allowed_address=thermo
        )

    return send_email, message


@periodic_task(run_every=timedelta(minutes=1))
def check_devices():

    thermos = AllowedAddress.objects.all()

    for thermo in thermos:
        ip = thermo.ip
        response = ping(ip)

        if response.ret_code != 0:

            send_email, message = check_device_status(thermo, False)

        else:
            send_email, message = check_device_status(thermo, True)

        if send_email:

            device_not_connected_mail(thermo, message)