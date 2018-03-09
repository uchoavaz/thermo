# -*- coding: utf-8 -*-

from pyping import ping
from celery import shared_task
from .models import AllowedAddress


@shared_task
def check_devices():

	thermos = AllowedAddress.objects.all()

	for thermo in thermos:
		thermo.ip
		response = pyping.ping(ip)

		if response.ret_code == 0:
		    print("IP: {0} is reachable").format(ip)
		else:
		    print("IP: {0} is not reachable").format(ip)