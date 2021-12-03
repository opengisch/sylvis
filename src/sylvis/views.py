from django.contrib import admin
from django.core.serializers import serialize
from django.db.models import Max
from django.shortcuts import get_object_or_404, render

from .models import Plot, Sector


def plot_view(request, plot_id):
    plot = get_object_or_404(Plot, id=plot_id)
    return render(
        request,
        "sylvis/aggregate_view.html",
        {
            "entity": plot,
            # django-admin integration (stuff like side-menu, breadcrumbs...)
            # see https://github.com/django/django/blob/97e9a84d2746f76a635455c13bd512ea408755ac/django/contrib/admin/options.py#L1642-L1655
            **admin.site.each_context(request),
            "opts": plot._meta,
            "title": str(plot),
            "subtitle": str(plot),
            "object_id": plot.pk,
            "original": plot,
        },
    )


def sector_view(request, sector_id):
    sector = get_object_or_404(Sector, id=sector_id)
    return render(
        request,
        "sylvis/aggregate_view.html",
        {
            "entity": sector,
            # django-admin integration (stuff like side-menu, breadcrumbs...)
            # see https://github.com/django/django/blob/97e9a84d2746f76a635455c13bd512ea408755ac/django/contrib/admin/options.py#L1642-L1655
            **admin.site.each_context(request),
            "opts": sector._meta,
            "title": str(sector),
            "subtitle": str(sector),
            "object_id": sector.pk,
            "original": sector,
        },
    )


def map_view(request):
    plots = Plot.objects.all()
    plots_geojson = serialize(
        "geojson",
        plots,
        geometry_field="geom",
        fields=("name",),
    )

    # TODO: simplify polygons with something like
    # from django.contrib.gis.db.models.functions import GeomOutputGeoFunc
    # class STSimplify(GeomOutputGeoFunc):
    #     function = 'ST_SIMPLIFY'
    #     arity = 2
    # plots = plots.annotate(geom_simple=STSimplify("geom", Value(10.0)))

    sectors = Sector.objects.all()
    max_level = sectors.aggregate(max_level=Max("level"))["max_level"]
    sectors_geojsons = []
    for level in range(0, max_level + 1):
        sectors_geojson = serialize(
            "geojson",
            sectors.filter(level=level),
            geometry_field="computed_geom",
            fields=("name", "level"),
        )
        sectors_geojsons.append(sectors_geojson)

    return render(
        request,
        "sylvis/map.html",
        {
            "plots_geojson": plots_geojson,
            "sectors_geojsons": f"[{','.join(sectors_geojsons)}]",
            # django-admin integration (stuff like side-menu, breadcrumbs...)
            # see https://github.com/django/django/blob/97e9a84d2746f76a635455c13bd512ea408755ac/django/contrib/admin/options.py#L1642-L1655
            **admin.site.each_context(request),
        },
    )
