from django.contrib import admin
from django.contrib.gis.db import models
from django.forms import widgets
from django.urls import path
from django.utils.html import format_html
from django.utils.translation import gettext as _
from mptt.admin import MPTTModelAdmin

from . import views
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
    list_display = ["__str__", "sectors_", "view_on_site_"]
    search_fields = ["name"]
    autocomplete_fields = ["sector"]
    inlines = [SectionInline, TreatmentInline, InventoryInline]

    def view_on_site_(self, obj=None):
        return format_html('<a href="{}">view</a>', obj.get_absolute_url())

    def get_urls(self):
        return [
            path(
                "<uuid:plot_id>/aggregate/",
                self.admin_site.admin_view(views.plot_view),
                name="plot_view",
            ),
            *super().get_urls(),
        ]

    def sectors_(self, obj):
        return " > ".join([a.name for a in obj.sector.get_ancestors()])


class BaseDataAdmin(admin.ModelAdmin):
    autocomplete_fields = ["plot"]


# Ugly hack to add custom links in django admin


class DummyMapModel(models.Model):
    class Meta:
        verbose_name_plural = _("Main map")
        app_label = "sylvis"
        managed = False


@admin.register(DummyMapModel)
class DummyMapModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        return [
            path(
                "map/",
                self.admin_site.admin_view(views.map_view),
                name=f"{self.model._meta.app_label}_{self.model._meta.model_name}_changelist",
            ),
        ]
