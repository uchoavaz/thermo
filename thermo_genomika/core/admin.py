from django.contrib import admin
from .models import SystemInfo

class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ('brand', 'designed_by', 'version','date')


admin.site.register(SystemInfo, SystemInfoAdmin)
