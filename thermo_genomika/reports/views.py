
# -*- coding: utf-8 -*-
import subprocess
import tempfile
from django.core.exceptions import ObjectDoesNotExist
from core.views import SystemInfoView
from core.views import correct_date_get_request
from account.views import LoginRequiredView
from django.http import HttpResponse
from django.views.generic import ListView
from catcher.models import ThermoInfo
from catcher.models import AllowedAddress
from django.contrib import messages
from django.utils import timezone
from checklist.models import DeviceChecklist
from fdfgen import forge_fdf
import babel.dates
import csv
import os


class FullReportView(LoginRequiredView, SystemInfoView, ListView):
    template_name = "full_report.html"
    model = ThermoInfo

    def generate_csv(self, file_name, date_str, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = \
            'attachment; filename="{0}_thermo_report_complete{1}.csv"'.format(
                file_name, date_str)

        writer = csv.writer(response, delimiter=',')
        header = [
            ThermoInfo._meta.get_field("temperature").verbose_name.title(),
            AllowedAddress._meta.get_field(
                "local").verbose_name.title(),
            AllowedAddress._meta.get_field("ip").verbose_name.title(),
            AllowedAddress._meta.get_field(
                "max_temperature").verbose_name.title(),
            AllowedAddress._meta.get_field(
                "min_temperature").verbose_name.title(),
            AllowedAddress._meta.get_field(
                "measure").verbose_name.title(),
            ThermoInfo._meta.get_field("allowed_temp").verbose_name.title(),
            ThermoInfo._meta.get_field("capture_date").verbose_name.title()
        ]
        writer.writerow(header)

        for line in queryset:
            temperature = timezone.get_current_timezone().normalize(
                line.capture_date)
            writer.writerow([
                str(line.temperature),
                line.device_ip.local,
                line.device_ip.ip,
                line.device_ip.max_temperature,
                line.device_ip.min_temperature,
                line.device_ip.get_measure_display().encode('ascii', 'ignore'),
                line.allowed_temp,
                temperature.strftime('%d-%m-%Y %H:%M')
            ])
        return response

    def dispatch(self, request, *args, **kwargs):
        request = self.request.GET

        if self.request.GET:
            local_pk = self.request.GET.get('local_pk')
            start_date = request.get('start_date')
            end_date = request.get('end_date')

            try:
                get = correct_date_get_request(
                    self.request, start_date, end_date)
                start_date = get['start_date']
                end_date = get['end_date']

                allowed_address = AllowedAddress.objects.get(pk=int(local_pk))
                queryset = self.get_queryset().filter(
                    device_ip=allowed_address)
                start_date_str = ''
                end_date_str = ''
                date_str = ''

                if start_date != '':
                    queryset = queryset.filter(capture_date__gte=start_date)
                    start_date_str = start_date.strftime('%d_%m_%Y')
                if end_date != '':
                    queryset = queryset.filter(capture_date__lte=end_date)
                    end_date_str = end_date.strftime('%d_%m_%Y')

                if start_date_str != '' or end_date_str != '':
                    date_str = "_" + start_date_str + "__to__" + end_date_str
                queryset = queryset.order_by('capture_date')

                return self.generate_csv(
                    allowed_address.local, date_str, queryset)
            except (ValueError, ObjectDoesNotExist):
                messages.error(
                    self.request, 'Local inexistente')
            except TypeError:
                messages.error(
                    self.request, 'Insira um Local')
            except Exception as err:
                messages.error(
                    self.request, err)
            return super(
                FullReportView, self).dispatch(
                self.request, *args, **kwargs)

        else:
            return super(
                FullReportView, self).dispatch(
                self.request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FullReportView, self).get_context_data(**kwargs)
        context['room_list'] = AllowedAddress.objects.all().distinct('local')
        return context


class AuditedReportView(LoginRequiredView, SystemInfoView, ListView):
    template_name = "audited_report.html"
    model = DeviceChecklist

    def dispatch(self, request, *args, **kwargs):

        request = self.request.GET

        if self.request.GET:
            local_pk = self.request.GET.get('local_pk')
            start_date = request.get('start_date')
            end_date = request.get('end_date')

            try:
                get = correct_date_get_request(
                    self.request, start_date, end_date)
                start_date = get['start_date']
                end_date = get['end_date']
                if end_date.year - start_date.year != 0:
                    raise Exception(
                        "Relatório não pode estar em anos diferentes !")

                if end_date.month - start_date.month != 0:
                    raise Exception(
                        "Relatório não pode estar em meses diferentes !")

                allowed_address = AllowedAddress.objects.get(pk=int(local_pk))

                return self.pdf(allowed_address, start_date, end_date)

            except (ValueError, ObjectDoesNotExist):
                messages.error(
                    self.request, 'Local inexistente')
            except TypeError:
                messages.error(
                    self.request, 'Insira um Local')
            except AttributeError:
                messages.error(
                    self.request, 'Insira uma data de inicio e fim')
            except Exception as err:
                messages.error(
                    self.request, err)
            return super(
                AuditedReportView, self).dispatch(
                self.request, *args, **kwargs)

        else:
            return super(
                AuditedReportView, self).dispatch(
                self.request, *args, **kwargs)

    def pdf(self, device, start_date, end_date):
        queryset = self.get_pdf_queryset(device, start_date, end_date)
        queryset = queryset.order_by('date')
        page_pdf_memory_data = tempfile.NamedTemporaryFile()
        fields = []

        self.get_fields(fields, queryset, device)
        inmemory_file = self.generate_pdf(fields, page_pdf_memory_data)
        initial_period = start_date.strftime('%d_%m_%Y')
        final_perdiod = end_date.strftime('%d_%m_%Y')
        file_name_period = initial_period + "_to_" + final_perdiod

        response = HttpResponse(content_type='text/pdf')
        inmemory_file.seek(0)
        response.write(inmemory_file.read())
        response['Content-Disposition'] = \
            'attachment; filename={0}_thermo_report_audited_{1}.pdf; charset=utf-8'.format(
                device.local.replace(' ', '_'), file_name_period)

        return response

    def get_fields(self, fields, queryset, device):
        try:
            count = 1

            measure = device.get_measure_display()

            size_temp_allwd = str(device.min_temperature) + " " + measure + " - " + \
                str(device.max_temperature) + " " + measure

            month = queryset[0].date
            month = babel.dates.format_date(month, 'MMMM', locale='pt_br')
            year = queryset[0].date.strftime('%Y')

            fields.append(('local', device.local))
            fields.append(('limites', size_temp_allwd))
            fields.append(('mes', month.title()))
            fields.append(('ano', year))
            fields.append(('ident', device.device_name))

            for field in queryset:
                avg_temp = str(field.avg_temp).replace('.', ',') + " " + measure
                min_temp = str(field.min_temp).replace('.', ',') + " " + measure
                max_temp = str(field.max_temp).replace('.', ',') + " " + measure
                fields.append(('dia{0}'.format(count), field.date.day))
                fields.append(('tempmedia{0}'.format(count), avg_temp))
                fields.append(('tempmaxima{0}'.format(count), max_temp))
                fields.append(('tempminima{0}'.format(count), min_temp))
                fields.append(('afericoes{0}'.format(count), field.admeasurements))
                fields.append(('nconform{0}'.format(count), field.temp_not_allwd))

                resp = '-'
                check_date = '-'

                try:
                    resp = field.responsible.username
                    check_date = field.check_date.strftime('%d-%m-%Y')
                except AttributeError:
                    pass
                fields.append(('resp{0}'.format(count), resp))
                fields.append(('datacheck{0}'.format(count), check_date))

                count = count + 1
        except IndexError:
            raise Exception(u"Dados não encontrados !")

    def generate_pdf(self, fields, page_pdf_memory_data):
        fdf = forge_fdf("", fields, [], [], [])
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = 'reports/pdfs_base/audited_report.pdf'
        base_pdf_directory = os.path.join(base_dir, path)

        process = subprocess.Popen(
            ['pdftk', base_pdf_directory, 'fill_form', '-', 'output',
             '-', 'flatten'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        page_pdf_memory_data.write(process.communicate(input=fdf)[0])

        return page_pdf_memory_data

    def get_pdf_queryset(self, device, start_date, end_date):
        queryset = self.get_queryset().filter(device=device)
        queryset = queryset.filter(date__gte=start_date)
        queryset = queryset.filter(date__lte=end_date)
        return queryset.order_by('date')

    def get_context_data(self, **kwargs):
        context = super(AuditedReportView, self).get_context_data(**kwargs)
        context['room_list'] = AllowedAddress.objects.all().distinct('local')
        return context

report = FullReportView.as_view()
audited_report = AuditedReportView.as_view()
