
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse_lazy
from django.contrib import auth
from django.shortcuts import redirect
from accounts.models import ThermoUser
from django.contrib import messages


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
                return redirect(reverse_lazy('core:home'))
            else:
                messages.error(request, u'Usuário não está ativo')
        else:
            messages.error(request, u'Usuário ou senha não existente')
    return render(request, template_name, context)


def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy('account:login'))
