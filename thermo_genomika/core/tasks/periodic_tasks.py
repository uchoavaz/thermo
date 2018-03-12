# -*- coding: utf-8 -*-

from pyping import ping
from datetime import timedelta
from core.models import DeviceStatus
from catcher.models import AllowedAddress
from celery.task.base import periodic_task
from mailer.tasks import device_not_connected_mail

def check_device_status(thermo, device_online):

    send_email = False
    message = ''

    device_status = DeviceStatus.objects.get(allowed_address__ip=thermo.ip)

    if device_status:
        pass

    else:
        check = False
        if device_online:
            check = True

        DeviceStatus.objects.create(
            first_check=check,
            allowed_address=thermo
        )

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