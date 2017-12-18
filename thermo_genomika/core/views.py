# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from account.views import LoginRequiredView
from django.views.generic import TemplateView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic import ListView
from catcher.models import ThermoInfo
from catcher.models import AllowedAddress
from .models import SystemInfo
from django.contrib import messages
from django.utils import timezone
from django.db.models import Max
from django.db.models import Min
from datetime import datetime


def correct_date_get_request(request, start_date, end_date):
    if start_date != '':
        try:
            start_date = datetime.strptime(start_date, "%d/%m/%Y")
        except (ValueError, UnicodeEncodeError):
            messages.error(
                request,
                u'Data início incorreta')
            start_date = ''
        except TypeError:
            start_date = ''

    if end_date != '':
        try:
            end_date = datetime.strptime(end_date, "%d/%m/%Y")
        except (ValueError, UnicodeEncodeError):
            messages.error(
                request, 'Data fim incorreta')
            end_date = ''
        except TypeError:
            end_date = ''
    if start_date != '' and end_date != '' \
            and (end_date - start_date).days < 0:
            raise Exception(
                u'Data fim maior que a data início')

    return {'start_date': start_date, 'end_date': end_date}


class SystemInfoView(ListView):

    def get_context_data(self, **kwargs):
        context = super(SystemInfoView, self).get_context_data(**kwargs)
        system_info = SystemInfo.objects.all()
        context['system_info'] = True
        context['request'] = self.request
        try:
            length = len(system_info)
            last_system_info = system_info[length - 1]
            context['brand'] = last_system_info.brand
            context['designed_by'] = last_system_info.designed_by
            context['version'] = last_system_info.version
        except AssertionError:
            context['brand'] = ''
            context['designed_by'] = ''
            context['version'] = ''
            context['system_info'] = False

        return context


class HomeView(LoginRequiredView, SystemInfoView, ListView):
    template_name = "home.html"
    model = ThermoInfo

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['registered_thermos'] = AllowedAddress.objects.all().count()
        context['total_temp'] = self.get_queryset().count()
        context['qtd_not_allowed_temp'] = self.get_queryset().filter(
            allowed_temp=False).count()
        return context


class ChartsView(LoginRequiredView, SystemInfoView, ListView):
    template_name = "charts.html"
    model = ThermoInfo

    def get_context_data(self, **kwargs):
        context = super(ChartsView, self).get_context_data(**kwargs)
        request = self.request.GET

        local_name = 'Genomika'
        date_list = []
        temp_list = []
        qtd_temp = 0
        max_temp_treat = '-'
        min_temp_treat = '-'
        max_temp_date = ''
        min_temp_date = ''
        last_temp = '-'
        last_temp_date = ''
        start_date_begin = ''
        end_date_begin = ''

        if request:
            local_pk = request.get('local_pk')
            start_date = request.get('start_date')
            end_date = request.get('end_date')

            start_date_begin = start_date
            end_date_begin = end_date
            try:

                get = correct_date_get_request(
                    self.request, start_date, end_date)
                start_date = get['start_date']
                end_date = get['end_date']

                allowed_address = AllowedAddress.objects.get(pk=int(local_pk))
                queryset = self.get_queryset().filter(
                    device_ip=allowed_address)
                if start_date != '':
                    queryset = queryset.filter(capture_date__gte=start_date)
                if end_date != '':
                    queryset = queryset.filter(capture_date__lte=end_date)
                queryset = queryset.order_by('capture_date')
                local_name = allowed_address.local
                date_list = self.get_date_list_string(queryset)
                temp_list = self.get_temp_list_string(queryset)
                qtd_temp = queryset.count()

                measure = allowed_address.get_measure_display()

                max_temp = queryset.aggregate(
                    Max('temperature'))['temperature__max']
                if max_temp is not None:
                    max_temp_treat = str(max_temp) + " " + measure

                min_temp = queryset.aggregate(
                    Min('temperature'))['temperature__min']

                if min_temp is not None:
                    min_temp_treat = str(min_temp) + " " + measure

                try:
                    min_temp_length = queryset.filter(
                        temperature=min_temp).count()
                    max_temp_length = queryset.filter(
                        temperature=max_temp).count()
                    last_position = queryset[queryset.count() - 1]
                    last_temp = str(last_position.temperature) + " " + measure
                    min_temp_date = queryset.filter(
                        temperature=min_temp)[min_temp_length - 1].capture_date
                    min_temp_date = timezone.get_current_timezone().normalize(
                        min_temp_date)
                    max_temp_date = queryset.filter(
                        temperature=max_temp)[max_temp_length - 1].capture_date
                    max_temp_date = timezone.get_current_timezone().normalize(
                        max_temp_date)
                    last_temp_date = timezone.get_current_timezone().normalize(
                        last_position.capture_date)
                    last_temp_date = last_temp_date.strftime('%d-%m-%Y %H:%M')
                    min_temp_date = min_temp_date.strftime('%d-%m-%Y %H:%M')
                    max_temp_date = max_temp_date.strftime('%d-%m-%Y %H:%M')
                except AssertionError:
                    pass

            except (ValueError, ObjectDoesNotExist):
                messages.error(
                    self.request, 'Local inexistente')
            except TypeError:
                messages.error(
                    self.request, 'Insira um Local')
            except Exception as err:
                messages.error(
                    self.request, err)

        context['start_date'] = start_date_begin
        context['end_date'] = end_date_begin
        context['last_temp'] = last_temp
        context['last_temp_date'] = last_temp_date
        context['min_temp'] = min_temp_treat
        context['max_temp'] = max_temp_treat
        context['min_temp_date'] = min_temp_date
        context['max_temp_date'] = max_temp_date
        context['qtd_temp'] = qtd_temp
        context['local_name'] = local_name
        context['date_list'] = date_list
        context['temp_list'] = temp_list
        context['room_list'] = AllowedAddress.objects.all().distinct('local')

        return context

    def get_date_list_string(self, queryset):
        date_list = []
        for query in queryset:
            date = timezone.localtime(query.capture_date)
            date = date.strftime('%d-%m-%Y %H:%M')
            date_list.append(date)

        return date_list

    def get_temp_list_string(self, queryset):
        temp_list = []
        for query in queryset:
            temp = query.temperature
            temp_list.append(temp)

        return temp_list


class DashboardsView(TemplateView):
    template_name = "dashboards.html"

    def get_context_data(self, **kwargs):
        context = super(DashboardsView, self).get_context_data(**kwargs)
        allowed_address = AllowedAddress.objects.get(pk=kwargs['local_id'])
        measure = allowed_address.get_measure_display()

        queryset = ThermoInfo.objects.filter(
            device_ip=allowed_address)
        queryset = queryset.order_by('capture_date')

        today_date = datetime.today().date()
        start_date_today = datetime(today_date.year, today_date.month, today_date.day)
        end_date_today = datetime(today_date.year, today_date.month, today_date.day, 23,59,59)
        queryset = queryset.filter(capture_date__gte=start_date_today)
        queryset = queryset.filter(capture_date__lte=end_date_today)
        
        try:
            last_position = queryset[queryset.count() - 1]
    
            max_temp = queryset.aggregate(
                Max('temperature'))['temperature__max']
            if max_temp is not None:
                max_temp_treat = str(max_temp) + " " + measure
    
            min_temp = queryset.aggregate(
                Min('temperature'))['temperature__min']
    
            if min_temp is not None:
                min_temp_treat = str(min_temp) + " " + measure
            
            last_temp = str(last_position.temperature) + " " + measure
    
            min_temp_length = queryset.filter(
                temperature=min_temp).count()
            max_temp_length = queryset.filter(
                temperature=max_temp).count()
            min_temp_date = queryset.filter(
                temperature=min_temp)[min_temp_length - 1].capture_date
            min_temp_date = timezone.get_current_timezone().normalize(
                min_temp_date)
            max_temp_date = queryset.filter(
                temperature=max_temp)[max_temp_length - 1].capture_date
            max_temp_date = timezone.get_current_timezone().normalize(
                max_temp_date)
            last_temp_date = timezone.get_current_timezone().normalize(
                last_position.capture_date)
    
            last_temp_date_treated = last_temp_date.strftime('Hoje às %H:%M')
            min_temp_date = min_temp_date.strftime('Hoje às %H:%M')
            max_temp_date = max_temp_date.strftime('Hoje às %H:%M')
    
            play_horn = self.request.GET.get('play_horn')
            horn = 'false'
            if allowed_address.min_temperature <= float(last_position.temperature) and \
                    float(last_position.temperature) < (allowed_address.max_temperature - 2):
                last_temp_color = '#339933'
                play_horn = 'false'
    
            elif float(last_position.temperature) >= allowed_address.max_temperature - 2 \
                    and float(last_position.temperature) <= allowed_address.max_temperature:
                last_temp_color = '#e6b800'
                play_horn = 'false'
            else:
                time_now = self.request.GET.get('time_now')
                if time_now != last_temp_date.strftime('%H:%M'):
                    play_horn = 'false'
                if (time_now == last_temp_date.strftime('%H:%M')) and (play_horn == 'false' or play_horn is None):
                    horn = 'true'
    
                if self.request.GET.get('bk_color') == '#e6b800':
                    last_temp_color = '#ff3333'
                else:
                    last_temp_color = '#e6b800'
        except AssertionError:
            last_temp_color = "#000000"
            horn = 'false'
            play_horn = 'false'
            last_temp = '-'
            max_temp_treat = '-'
            min_temp_treat = '-'
            min_temp_date ='-' 
            max_temp_date = '-'
            last_temp_date_treated = '-'
            last_temp_color = '-'
            
            
        context['local_pk'] = kwargs['local_id']
        context['horn'] = horn
        context['play_horn'] = play_horn
        context['time_now'] = datetime.today().strftime('%H:%M')
        context['local_name'] = allowed_address.local
        context['last_temp'] = last_temp
        context['max_temp'] = max_temp_treat
        context['min_temp'] = min_temp_treat
        context['min_temp_date'] = min_temp_date
        context['max_temp_date'] = max_temp_date
        context['last_temp_date'] = last_temp_date_treated
        context['last_temp_color'] = last_temp_color
        return context


class GuiDashboard(DashboardsView):
    template_name = 'tr_body_dashboard.html'


gui_dashboard = GuiDashboard.as_view()
home = HomeView.as_view()
charts = ChartsView.as_view()
dashboards = DashboardsView.as_view()
