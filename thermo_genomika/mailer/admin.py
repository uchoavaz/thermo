from django.contrib import admin
from .models import MailLog
from .models import Recipient


class MailLogAdmin(admin.ModelAdmin):
    search_fields = ['local', 'temperature', 'situation', 'recipient_list']
    list_display = (
        'local',
        'temperature',
        'situation',
        'recipient_list',
        'date',
    )


class RecipientAdmin(admin.ModelAdmin):
    search_fields = ['email', 'is_active']
    list_display = (
        'email',
        'is_active',
    )

admin.site.register(Recipient, RecipientAdmin)
admin.site.register(MailLog, MailLogAdmin)
