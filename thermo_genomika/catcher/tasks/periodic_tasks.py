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

        if device_line and not device_status.last_connection and not device_status.previous_last_connection:
            device_status.check_offline = False
            send_email = True
            message = "Dispositivo Online !"

        elif not device_line and not device_status.last_connection and not device_status.check_offline:
            device_status.check_offline = True
            send_email = True

        device_status.previous_last_connection = device_status.last_connection
        device_status.last_connection = device_line
        device_status.check_date = timezone.get_current_timezone().normalize(timezone.now())
        device_status.save()

    else:

        if device_line:
            message = "Dispositivo Online !"
            send_email = True

        DeviceStatus.objects.create(
            check_offline=False,
            last_connection=device_line,
            allowed_address=thermo
        )

    return send_email, message

def false_positive_check(ip):

    check_list = [False] * 4

    for pos, _ in enumerate(check_list):

        response = ping(ip)

        if response.ret_code != 0:

            check_list[pos] = False

        else:

            check_list[pos] = True

    return any(check_list)

@periodic_task(run_every=timedelta(minutes=1))
def check_devices():

    thermos = AllowedAddress.objects.all()

    for thermo in thermos:
        ip = thermo.ip
        response = false_positive_check(ip)

        if response:

            send_email, message = check_device_status(thermo, True)
            
        else:

            send_email, message = check_device_status(thermo, False)

        if send_email:

            device_not_connected_mail(thermo, message)
