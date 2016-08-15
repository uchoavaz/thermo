from django.contrib import admin
from .models import DeviceChecklist

class DeviceChecklistAdmin(admin.ModelAdmin):
    search_fields = [
        'device',
        'max_temp',
        'min_temp',
        'avg_temp',
        'date_max_temp',
        'date_min_temp',
        'responsible',
        'is_checked',
        'date',
        'temp_not_allwd',
        'admeasurements'
    ]
    list_display = (
        'date',
        'device',
        'max_temp',
        'min_temp',
        'avg_temp',
        'date_max_temp',
        'date_min_temp',
        'responsible',
        'is_checked',
        'temp_not_allwd',
        'admeasurements'
    )

admin.site.register(DeviceChecklist, DeviceChecklistAdmin)
