from django.contrib import admin
from .models import ThermoUser


class ThermoUserAdmin(admin.ModelAdmin):
    list_filter = ['email']
    list_display = (
        'email', 'is_staff',
        'is_active', 'is_superuser')


admin.site.register(ThermoUser, ThermoUserAdmin)