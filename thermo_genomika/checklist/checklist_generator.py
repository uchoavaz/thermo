
from django.core.exceptions import ObjectDoesNotExist
from .models import DeviceChecklist
from catcher.models import ThermoInfo
from django.db.models import Max
from django.db.models import Min
from django.db.models import Avg

class CheckListGenerator():
    temperature = None
    date = None

    def __init__(self, temperature, date):
        self.temperature = temperature
        self.date = date

    def check_db(self, temp, date):
        try:
            query = DeviceChecklist.objects.get(date=date)
            import ipdb;ipdb.set_trace()

            thermo_report = self.get_thermo_report()

        except ObjectDoesNotExist:
            pass

    def get_thermo_report(self):
        thermo_info = ThermoInfo.objects.all()

        info = {}

        info['avg'] = thermo_info.aggregate(
            Avg('temperature'))['temperature__avg']
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
        return info

    def generate(self):
        temp = self.temperature
        date = self.date
        self.check_db(temp, date)
