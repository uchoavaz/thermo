
# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from account.views import LoginRequiredView
from django.views.generic import ListView
from .models import DeviceChecklist
from core.views import SystemInfoView
from catcher.models import AllowedAddress
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from core.views import correct_date_get_request


class ChecklistView(LoginRequiredView, SystemInfoView, ListView):
    template_name = 'checklist.html'
    model = DeviceChecklist
    start_date = ''
    end_date = ''

    def get(self, request, *args, **kwargs):
        if self.request.GET:
            try:
                pk_request = self.request.GET.getlist('pk')
                for pk in pk_request:
                    DeviceChecklist.objects.filter(pk=pk).update(
                        is_checked=True, responsible=self.request.user)
                    messages.success(
                        request,
                        u'Checklist salvo')

            except ValueError:
                messages.error(
                    request,
                    u'PK inválido')

        return super(ChecklistView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ChecklistView, self).get_context_data(**kwargs)
        context['room_list'] = AllowedAddress.objects.all().distinct('local')
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        if self.get_queryset() is not None:
            if self.get_queryset().count() == 0:
                context['result_message'] = 'Sem resultados encontrados'
        return context

    def get_queryset(self):
        queryset = super(ChecklistView, self).get_queryset()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        local_pk = self.request.GET.get('local_pk')

        try:
            if local_pk is not None:
                allowed_address = AllowedAddress.objects.get(pk=int(local_pk))
                queryset = queryset.filter(
                    device=allowed_address)
                dates = correct_date_get_request(
                    self.request, start_date, end_date)
                if dates['start_date'] != '':
                    queryset = queryset.filter(date__gte=dates['start_date'])
                if dates['end_date'] != '':
                    queryset = queryset.filter(date__lte=dates['end_date'])
                if start_date is not None:
                    self.start_date = start_date
                if end_date is not None:
                    self.end_date = end_date
                return queryset

        except (ValueError, ObjectDoesNotExist):
            messages.error(
                self.request, 'Local inexistente')
        except Exception as err:
            messages.error(
                self.request, err)

checklist = ChecklistView.as_view()
