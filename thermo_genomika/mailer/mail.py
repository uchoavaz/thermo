
# -*- coding: utf-8 -*-
from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail_template(
        subject,
        template_name,
        context, recipient_list, from_email, fail_silently=False):

    message_html = render_to_string(template_name, context)

    message_txt = striptags(message_html)

    email = EmailMultiAlternatives(
        subject=subject, body=message_txt, from_email=from_email,
        to=recipient_list
    )
    email.attach_alternative(message_html, "text/html")
    email.send(fail_silently=fail_silently)


def send_mail(date, local, situation, recipient, temperature=None):
    date = date.strftime('%d-%m-%Y   %H:%M')
    subject = "Contato Thermo Genomika - {0} - Local: {1} - {2}".format(
        situation, local, date)

    context = {
        'local': local,
        'temperature': temperature,
        'situation': situation
    }

    template_name = 'contact_email.html'
    send_mail_template(
        subject,
        template_name,
        context,
        recipient, settings.CONTACT_EMAIL)