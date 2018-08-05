from django.contrib import admin

from wakfustrat.common.models import Zone, SubZone


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubZone)
class SubZoneAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
