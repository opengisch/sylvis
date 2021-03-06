import uuid
from collections import defaultdict

from computedfields.models import ComputedFieldsModel, computed
from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPolygon, Polygon
from django.urls import reverse
from django.utils.translation import gettext as _
from mptt.models import MPTTModel, TreeForeignKey


class Sector(MPTTModel, ComputedFieldsModel):
    class Meta:
        verbose_name = "  " + _("Sector")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    @computed(
        models.IntegerField(default=0),
        depends=[
            ["children", ["computed_sections_total"]],
            ["plots.section_set", ["id"]],
        ],
    )
    def computed_sections_total(self):
        return self.section_set.count()

    @computed(
        models.IntegerField(default=0),
        depends=[
            ["children", ["computed_inventories_total"]],
            ["plots.inventory_set", ["id"]],
        ],
    )
    def computed_inventories_total(self):
        return self.inventory_set.count()

    @computed(
        models.IntegerField(default=0),
        depends=[
            ["children", ["computed_treatments_total"]],
            ["plots.treatment_set", ["id"]],
        ],
    )
    def computed_treatments_total(self):
        return self.treatment_set.count()

    @computed(
        models.JSONField(default=dict),
        depends=[
            ["children", ["computed_sections_detail"]],
            ["plots.section_set", ["date", "volume"]],
        ],
    )
    def computed_sections_detail(self):
        counts = defaultdict(int)
        for section in self.section_set.exclude(date__isnull=True):
            counts[section.date.year] += 1
        return counts

    @computed(
        models.JSONField(default=dict),
        depends=[
            ["children", ["computed_inventories_detail"]],
            ["plots.inventory_set", ["date", "standing_volume"]],
        ],
    )
    def computed_inventories_detail(self):
        counts = defaultdict(int)
        for inventory in self.inventory_set.exclude(date__isnull=True):
            counts[inventory.date.year] += 1
        return counts

    @computed(
        models.JSONField(default=dict),
        depends=[
            ["children", ["computed_treatments_detail"]],
            ["plots.treatment_set", ["date"]],
        ],
    )
    def computed_treatments_detail(self):
        counts = defaultdict(int)
        for treatment in self.treatment_set.exclude(date__isnull=True):
            counts[treatment.date.year] += 1
        return counts

    @computed(
        models.MultiPolygonField(srid=2056, default=MultiPolygon),
        depends=[["children", ["computed_geom"]], ["plots", ["geom"]]],
    )
    def computed_geom(self):
        polygon = MultiPolygon()

        # Aggregate geometries from plots (buffered to join nearby polygons)
        for plot in self.plots.all():
            polygon = polygon.union(plot.geom.buffer(10))

        # Debuffer to retrieve original limits
        polygon = polygon.buffer(-10)

        # Aggregate geometries from child sectors
        for child in self.children.all():
            polygon = polygon.union(child.computed_geom)

        # Simplify
        polygon = polygon.simplify(5)

        # Force multipolygon
        if isinstance(polygon, Polygon):
            polygon = MultiPolygon([polygon])

        return polygon

    @property
    def plots_set(self):
        descendent_sectors = self.get_descendants(include_self=True)
        return Plot.objects.filter(sector__in=descendent_sectors)

    @property
    def section_set(self):
        descendent_sectors = self.get_descendants(include_self=True)
        return Section.objects.filter(plot__sector__in=descendent_sectors)

    @property
    def inventory_set(self):
        descendent_sectors = self.get_descendants(include_self=True)
        return Inventory.objects.filter(plot__sector__in=descendent_sectors)

    @property
    def treatment_set(self):
        descendent_sectors = self.get_descendants(include_self=True)
        return Treatment.objects.filter(plot__sector__in=descendent_sectors)

    def get_absolute_url(self):
        return reverse("sylvis:sector_detail", args=[self.id])

    def get_admin_url(self):
        return reverse("admin:sylvis_sector_change", args=[self.id])

    def __str__(self):
        return self.name


class Plot(models.Model):
    class Meta:
        verbose_name = " " + _("Plot")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    geom = models.MultiPolygonField(srid=2056, verbose_name=_("Geometry"))
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    sector = models.ForeignKey(
        Sector, on_delete=models.SET_NULL, blank=True, null=True, related_name="plots"
    )
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
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Yearly growth"),
        null=True,
        blank=True,
    )
    etale = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("sylvis:plot_detail", args=[self.id])

    def get_admin_url(self):
        return reverse("admin:sylvis_plot_change", args=[self.id])

    def __str__(self):
        return self.name


class BaseData(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, default="")


class Section(BaseData):
    class Meta:
        verbose_name = _("Section")
        ordering = ["date"]

    volume = models.DecimalField(max_digits=10, decimal_places=2)


class Treatment(BaseData):
    class Meta:
        verbose_name = _("Treatment")
        ordering = ["date"]

    description = models.TextField(blank=True, default="")


class Inventory(BaseData):
    class Meta:
        verbose_name = _("Inventory")
        ordering = ["date"]

    standing_volume = models.DecimalField(max_digits=10, decimal_places=2)
