from django.contrib import admin
from .models import SystemInfo
from .models import DeviceStatus

class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ('brand', 'designed_by', 'version','date')


class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ('last_connection', 'check_date', 'email_sent', 'allowed_address')

admin.site.register(SystemInfo, SystemInfoAdmin)
admin.site.register(DeviceStatus, DeviceStatusAdmin)
