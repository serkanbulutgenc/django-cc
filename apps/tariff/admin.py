from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

# Register your models here.
from apps.tariff.models import Tariff

# Register your models here.


@admin.register(Tariff)
class TariffAdminModel(DraggableMPTTAdmin):
    mptt_level_indent = 10
    list_display = ["tree_actions", "level", "indented_title"]
    list_display_links = ["indented_title"]
