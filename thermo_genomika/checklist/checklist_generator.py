
from django.core.exceptions import ObjectDoesNotExist
from .models import DeviceChecklist
from catcher.models import ThermoInfo
from django.db.models import Max
from django.db.models import Min
from django.db.models import Avg
from django.utils import timezone


class CheckListGenerator():
    temperature = None
    date = None
    device = None
    log = ''

    def __init__(self, device, temperature, date):
        self.device = device
        self.temperature = temperature
        self.date = date

    def check_db(self, device, temp, date):
        thermo_report = self.get_thermo_report(date, device)
        try:
            check = DeviceChecklist.objects.get(date=date, device=device)
            check.avg_temp = thermo_report['avg_temp']
            check.max_temp = thermo_report['max_temp']
            check.min_temp = thermo_report['min_temp']
            check.date_max_temp = thermo_report['date_max_temp']
            check.date_min_temp = thermo_report['date_min_temp']
            check.temp_not_allwd = thermo_report['temp_not_allwd']
            check.admeasurements = thermo_report['admeasurements']
            check.save()
            self.log = 'Checklist atualizado com sucesso'
        except ObjectDoesNotExist:
            DeviceChecklist.objects.create(
                date=date,
                device=device,
                avg_temp=thermo_report['avg_temp'],
                max_temp=thermo_report['max_temp'],
                min_temp=thermo_report['min_temp'],
                date_max_temp=thermo_report['date_max_temp'],
                date_min_temp=thermo_report['date_min_temp'],
                admeasurements=thermo_report['admeasurements'],
                temp_not_allwd=thermo_report['temp_not_allwd'],
            )
            self.log = 'Novo checklist criado'

    def get_thermo_report(self, date, device):
        current_tz = timezone.get_current_timezone().normalize(date)
        thermo_info = ThermoInfo.objects.filter(
            device_ip=device,
            capture_date__day=current_tz.day,
            capture_date__month=current_tz.month,
            capture_date__year=current_tz.year,
        )
        info = {}
        avg_temp = str(thermo_info.aggregate(
            Avg('temperature'))['temperature__avg'])
        avg_temp = avg_temp[0:(avg_temp.index('.') + 2)]
        info['avg_temp'] = avg_temp
        info['max_temp'] = thermo_info.aggregate(
            Max('temperature'))['temperature__max']
        info['min_temp'] = thermo_info.aggregate(
            Min('temperature'))['temperature__min']

        min_temp_length = thermo_info.filter(
            temperature=info['min_temp']).count()
        max_temp_length = thermo_info.filter(
            temperature=info['max_temp']).count()

        info['date_max_temp'] = thermo_info.filter(
            temperature=info['max_temp'])[max_temp_length - 1].capture_date
        info['date_min_temp'] = thermo_info.filter(
            temperature=info['min_temp'])[min_temp_length - 1].capture_date
        info['temp_not_allwd'] = thermo_info.filter(allowed_temp=False).count()
        info['admeasurements'] = thermo_info.count()
        return info

    def checklist_log(self):
        return self.log

    def generate(self):
        temp = self.temperature
        date = self.date
        device = self.device
        self.check_db(device, temp, date)
