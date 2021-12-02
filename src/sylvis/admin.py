from django.contrib import admin
from django.contrib.gis.db import models
from django.forms import widgets
from django.urls import path
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from . import views
from .models import Inventory, Plot, Section, Sector, Treatment


@admin.register(Sector)
class SectorAdmin(MPTTModelAdmin):
    list_display = ["__str__", "view_on_site_"]
    search_fields = ["name"]
    # autocomplete_fields = ["parent"]  # see https://github.com/django-mptt/django-mptt/issues/800

    def view_on_site_(self, obj=None):
        return format_html('<a href="{}">view</a>', obj.get_absolute_url())

    def get_urls(self):
        custom_urls = [
            path(
                "<uuid:sector_id>/aggregate/",
                self.admin_site.admin_view(views.sector_view),
                name="sector_view",
            ),
        ]
        return custom_urls + super().get_urls()


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
    list_display = ["__str__", "sector", "view_on_site_"]
    search_fields = ["name"]
    autocomplete_fields = ["sector"]
    inlines = [SectionInline, TreatmentInline, InventoryInline]

    def view_on_site_(self, obj=None):
        return format_html('<a href="{}">view</a>', obj.get_absolute_url())

    def get_urls(self):
        custom_urls = [
            path(
                "<uuid:plot_id>/aggregate/",
                self.admin_site.admin_view(views.plot_view),
                name="plot_view",
            ),
        ]
        return custom_urls + super().get_urls()


class BaseDataAdmin(admin.ModelAdmin):
    autocomplete_fields = ["plot"]
