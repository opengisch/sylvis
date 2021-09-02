from django.contrib.gis.db import models
from django.utils.translation import gettext as _


class SectorA(models.Model):
    class Meta:
        verbose_name = "  " + _("Level A sector")

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SectorB(models.Model):
    class Meta:
        verbose_name = "  " + _("Level B sector")

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        SectorA, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name


class SectorC(models.Model):
    class Meta:
        verbose_name = "  " + _("Level C sector")

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        SectorB, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Plot(models.Model):
    class Meta:
        verbose_name = " " + _("Plot")

    geom = models.PolygonField(srid=2056)
    name = models.CharField(max_length=255)
    sector = models.ForeignKey(
        SectorC, on_delete=models.SET_NULL, blank=True, null=True
    )
    rotation_sections = models.IntegerField(default=0)
    rotation_treatments = models.IntegerField(default=0)
    planned_next_section = models.DateField(blank=True, null=True)
    planned_next_treatment = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


class BaseData(models.Model):
    class Meta:
        abstract = True

    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, default="")


class Section(BaseData):
    class Meta:
        verbose_name = _("Section")

    volume = models.DecimalField(max_digits=10, decimal_places=2)


class Treatment(BaseData):
    class Meta:
        verbose_name = _("Treatment")

    description = models.TextField(blank=True, default="")


class Inventory(BaseData):
    class Meta:
        verbose_name = _("Inventory")

    vol_s_pied = models.DecimalField(max_digits=10, decimal_places=2)
