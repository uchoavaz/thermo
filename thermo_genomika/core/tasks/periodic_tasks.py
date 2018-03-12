# -*- coding: utf-8 -*-

from pyping import ping
from datetime import timedelta
from catcher.models import AllowedAddress
from celery.task.base import periodic_task
from mailer.tasks import device_not_connected_mail


@periodic_task(run_every=timedelta(seconds=1))
def check_devices():

	thermos = AllowedAddress.objects.all()

	for thermo in thermos:
		ip = thermo.ip
		response = ping(ip)

		if response.ret_code == 0:
		    print("IP: {0} is reachable").format(ip)
		else:
		    device_not_connected_mail(thermo)