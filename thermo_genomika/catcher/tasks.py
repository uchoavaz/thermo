
from .models import AllowedAddress
from .models import ThermoInfo
from .models import ThermoLog
from django.utils import timezone
import datetime


def delete_old_records(ip):
    log = 'No old records deleted'
    days_to_delete = AllowedAddress.objects.get(ip=ip).days_to_delete

    if days_to_delete > 0:
        current_tz = timezone.get_current_timezone().normalize(timezone.now())
        days_ago = (current_tz - datetime.timedelta(days=days_to_delete))
        thermo_info = ThermoInfo.objects.filter(
            capture_date__lte=days_ago)
        if len(thermo_info) > 0:
            log = "Old records in ThermoInfo deleted"
            thermo_info.delete()

        thermo_log = ThermoLog.objects.filter(
            capture_date__lte=days_ago, device_ip=ip)

        if len(thermo_info) > 0:
            log = log + ", " + "Old records in ThermoLog deleted"
            thermo_log.delete()

    return log
