from django.contrib import admin
from django.contrib.gis.db import models
from django.forms import widgets
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


class BaseDataInline(admin.TabularInline):
    extra = 0
    formfield_overrides = {
        models.TextField: {"widget": widgets.Textarea(attrs={"rows": 2})},
    }


class SectionInline(BaseDataInline):
    model = Section


class TreatmentInline(BaseDataInline):
    model = Treatment


class InventoryInline(BaseDataInline):
    model = Inventory


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ["__str__", "sectors_", "view_on_site_"]
    search_fields = ["name"]
    autocomplete_fields = ["sector"]
    inlines = [SectionInline, TreatmentInline, InventoryInline]

    def view_on_site_(self, obj=None):
        return format_html('<a href="{}">view</a>', obj.get_absolute_url())

    def sectors_(self, obj):
        return " > ".join([a.name for a in obj.sector.get_ancestors()])


class BaseDataAdmin(admin.ModelAdmin):
    autocomplete_fields = ["plot"]
