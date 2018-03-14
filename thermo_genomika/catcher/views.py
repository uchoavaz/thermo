
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.http import HttpResponse
from .models import ThermoInfo
from .models import AllowedAddress
from .models import ThermoLog
from ipware.ip import get_ip
from mailer.tasks import warn_mail
from .tasks.tasks import delete_old_records
from checklist.checklist_generator import CheckListGenerator
from django.utils import timezone


class CatcherView(TemplateView):

    def get(self, request, *args, **kwargs):
        log = ''
        request = self.request
        ip = get_ip(request)
        error = True

        try:
            temperature = request.GET.get('temp')
            if temperature is None:
                raise Exception("Temperature is not in request")

            temperature = float(temperature) / 1000
            log = 'Request received'
            allowed_address = AllowedAddress.objects.get(ip=ip)
            if allowed_address.is_active:

                thermo_info = ThermoInfo.objects.create(
                    temperature=temperature,
                    device_ip=allowed_address,
                    capture_date=timezone.now()
                )

                log = log + ", "'Data saved with success'

                email_log = warn_mail(
                    thermo_info)
                log = log + ", " + email_log
                delete_log = delete_old_records(allowed_address)
                log = log + ", " + delete_log

                checklist = CheckListGenerator(
                    allowed_address, temperature, timezone.now())
                checklist.generate()
                log = log + ", " + checklist.checklist_log()
            else:
                log = log + ", " + "Ip not active"
        except ObjectDoesNotExist as err:
            log = log + ", " + str(err)
            error = False

        except TypeError as err:
            log = log + ", " + str(err)
            error = False

        except Exception as err:
            log = log + ", " + ("Error:" + str(err))
            error = False

        ThermoLog.objects.create(
            request=request,
            log=log,
            device_ip=ip,
            all_worked=error
        )
        return HttpResponse('')


catcher = CatcherView.as_view()
