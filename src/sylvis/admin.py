from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from .models import Inventory, Plot, Section, Sector, Treatment


@admin.register(Sector)
class SectorAdmin(MPTTModelAdmin):
    list_display = ["__str__", "view_on_site_"]
    search_fields = ["name"]
    readonly_fields = [
        "computed_sections_total",
        "computed_inventories_total",
        "computed_treatments_total",
        "computed_sections_detail",
        "computed_inventories_detail",
        "computed_treatments_detail",
    ]
    # autocomplete_fields = ["parent"]  # see https://github.com/django-mptt/django-mptt/issues/800

    def view_on_site_(self, obj=None):
        return format_html('<a href="{}">view</a>', obj.get_absolute_url())


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ["name", "sector", "view_on_site_"]
    list_display_links = ["name"]
    search_fields = ["name"]
    autocomplete_fields = ["sector"]
    ordering = ["sector"]

    def view_on_site_(self, obj=None):
        return format_html('<a href="{}">view</a>', obj.get_absolute_url())

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("sector")


class BaseDataAdmin(admin.ModelAdmin):
    class PlotFilter(AutocompleteFilter):
        title = "Plot"
        field_name = "plot"

    list_display = ["date", "plot"]
    ordering = ["-date"]
    autocomplete_fields = ["plot"]
    date_hierarchy = "date"
    list_filter = [PlotFilter]


@admin.register(Section)
class SectionAdmin(BaseDataAdmin):
    list_display = BaseDataAdmin.list_display + ["volume"]


@admin.register(Inventory)
class InventoryAdmin(BaseDataAdmin):
    list_display = BaseDataAdmin.list_display + ["standing_volume"]


@admin.register(Treatment)
class TreatmentAdmin(BaseDataAdmin):
    pass
