# -*- coding: utf-8 -*-

from pyping import ping
from datetime import timedelta
from core.models import DeviceStatus
from catcher.models import AllowedAddress
from celery.task.base import periodic_task
from mailer.tasks import device_not_connected_mail

def check_device_status(thermo, device_line):

    send_email = False
    message = 'Dispositivo Offline !'

    devices_status = DeviceStatus.objects.filter(allowed_address__ip=thermo.ip)

    if devices_status:
        device_status = devices_status[0]

        if device_status.second_check is None:
            device_status.second_check = device_line

        else:
            if device_status.first_cursor:

                device_status.first_check = device_line
                device_status.first_cursor = False

            else:
                device_status.second_check = device_line
                device_status.first_cursor = True

        device_status.save()
        send_email = ( (not device_status.first_check) and (not device_status.second_check) or ( (not device_status.first_check) and device_status.second_check )

        if device_status.first_check == False and device_status.second_check == True:
            message = "Dispositivo Online !"
        print send_email
        print device_status.first_check
        print device_status.second_check
        print message
    else:
        check = False
        if device_line:
            check = True
            message = "Dispositivo Online !"

        DeviceStatus.objects.create(
            first_check=check,
            allowed_address=thermo
        )

        send_email = True

    return send_email, message


@periodic_task(run_every=timedelta(minutes=5))
def check_devices():

    thermos = AllowedAddress.objects.all()

    for thermo in thermos:
        ip = thermo.ip
        response = ping(ip)

        if response.ret_code != 0:

            send_email, message = check_device_status(thermo, False)

            if send_email:

                device_not_connected_mail(thermo, message)

        else:
            check_device_status(thermo, True)