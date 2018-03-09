# -*- coding: utf-8 -*-

from pyping import ping
from celery.schedules import crontab
from catcher.models import AllowedAddress
from celery.task.base import periodic_task


@periodic_task(run_every=crontab(hour=0, minute=1))
def check_devices():

	thermos = AllowedAddress.objects.all()

	for thermo in thermos:
		ip = thermo.ip
		response = ping(ip)

		if response.ret_code == 0:
		    print("IP: {0} is reachable").format(ip)
		else:
		    print("IP: {0} is not reachable").format(ip)