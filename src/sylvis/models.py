import uuid

from django.contrib.gis.db import models
from django.urls import reverse
from django.utils.translation import gettext as _


class Sector(models.Model):
    class Meta:
        verbose_name = "  " + _("Sector")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def section_set(self):
        return Section.objects.filter(plot__sector=self)

    @property
    def inventory_set(self):
        return Inventory.objects.filter(plot__sector=self)

    @property
    def treatment_set(self):
        return Treatment.objects.filter(plot__sector=self)

    def get_absolute_url(self):
        return reverse("admin:sector_view", args=[self.id])

    def __str__(self):
        return self.name


class Plot(models.Model):
    class Meta:
        verbose_name = " " + _("Plot")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    geom = models.MultiPolygonField(srid=2056, verbose_name=_("Geometry"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL, blank=True, null=True)
    rotation_sections = models.IntegerField(
        null=True, blank=True, verbose_name=_("Section rotation rate")
    )
    rotation_treatments = models.IntegerField(
        null=True, blank=True, verbose_name=_("Treatment rotation rate")
    )
    planned_next_section = models.DateField(
        blank=True, null=True, verbose_name=_("Next planned section")
    )
    planned_next_treatment = models.DateField(
        blank=True, null=True, verbose_name=_("Next planned treatment")
    )
    yearly_growth = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Yearly growth"), null=True, blank=True
    )
    etale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("admin:plot_view", args=[self.id])

    def __str__(self):
        return self.name


class BaseData(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)


class Section(BaseData):
    class Meta:
        verbose_name = _("Section")

    volume = models.DecimalField(max_digits=10, decimal_places=2)


class Treatment(BaseData):
    class Meta:
        verbose_name = _("Treatment")

    description = models.TextField(blank=True, null=True)


class Inventory(BaseData):
    class Meta:
        verbose_name = _("Inventory")

    standing_volume = models.DecimalField(max_digits=10, decimal_places=2)
