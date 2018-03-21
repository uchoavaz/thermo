
from django.contrib import admin
from .models import ThermoInfo
from .models import AllowedAddress
from .models import ThermoLog
from .models import DeviceStatus


class ThermoInfoAdmin(admin.ModelAdmin):
    search_fields = [
        'allowed_temp',
        'capture_date', 'temperature', 'device_ip__ip', 'device_ip__local']
    list_display = (
        'temperature',
        'device_ip',
        'allowed_temp',
        'capture_date'
    )


class AllowedAddressAdmin(admin.ModelAdmin):
    search_fields = [
        'ip',
        'local',
        'is_active',
        'measure',
        'max_temperature',
        'min_temperature',
        'days_to_delete'
    ]
    list_display = (
        'ip',
        'local',
        'max_temperature',
        'min_temperature',
        'days_to_delete',
        'measure',
        'is_active',
    )


class ThermoLogAdmin(admin.ModelAdmin):
    search_fields = [
        'request', 'log', 'device_ip', 'capture_date', 'all_worked'
    ]
    list_display = (
        'request',
        'log',
        'device_ip',
        'all_worked',
        'capture_date',
    )


class DeviceStatusAdmin(admin.ModelAdmin):
    list_display = ('last_connection', 'previous_last_connection', 'check_date', 'check_offline', 'allowed_address')


admin.site.register(ThermoLog, ThermoLogAdmin)
admin.site.register(ThermoInfo, ThermoInfoAdmin)
admin.site.register(AllowedAddress, AllowedAddressAdmin)
admin.site.register(DeviceStatus, DeviceStatusAdmin)