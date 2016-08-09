
# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import auth
from django.shortcuts import redirect
from account.models import ThermoUser
from django.contrib import messages
from django.utils import timezone

def login(request):
    template_name = 'login.html'
    context = {}

    email = request.POST.get('email')
    password = request.POST.get('password')

    context['email_label'] = ThermoUser._meta.get_field(
        "email").verbose_name.title()
    context['password_label'] = ThermoUser._meta.get_field(
        "password").verbose_name.title()

    if email and password:
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                user.last_access = timezone.now()
                user.save()
                return redirect(reverse_lazy('core:home'))
            else:
                messages.error(request, u'Usuário não está ativo')
        else:
            messages.error(request, u'Usuário ou senha não existente')
    return render(request, template_name, context)


def logout(request):
    request.user.last_access = timezone.now()
    request.user.save()
    auth.logout(request)
    return redirect(reverse_lazy('account:login'))


class LoginRequiredView(LoginRequiredMixin):
    login_url = reverse_lazy("account:login")
