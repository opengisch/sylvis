from django.contrib import admin

from .models import Inventory, Plot, Section, SectorA, SectorB, SectorC, Treatment


class BaseSectorAdmin(admin.ModelAdmin):
    pass


@admin.register(SectorA)
class SectorAAdmin(BaseSectorAdmin):
    pass


@admin.register(SectorB)
class SectorBAdmin(BaseSectorAdmin):
    pass


@admin.register(SectorC)
class SectorCAdmin(BaseSectorAdmin):
    pass


class BaseDataInline(admin.TabularInline):
    extra = 0


class SectionInline(BaseDataInline):
    model = Section


class TreatmentInline(BaseDataInline):
    model = Treatment


class InventoryInline(BaseDataInline):
    model = Inventory


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    inlines = [
        SectionInline,
        TreatmentInline,
        InventoryInline,
    ]


class BaseDataAdmin(admin.ModelAdmin):
    autocomplete_fields = ["plot"]


@admin.register(Section)
class SectionAdmin(BaseDataAdmin):
    pass


@admin.register(Treatment)
class TreatmentAdmin(BaseDataAdmin):
    pass


@admin.register(Inventory)
class InventoryAdmin(BaseDataAdmin):
    pass
