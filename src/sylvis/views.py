from django.contrib import admin
from django.core.serializers import serialize
from datetime import date
from collections import defaultdict
from django.shortcuts import get_object_or_404, render
from bokeh.plotting import figure
from bokeh.embed import components
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

    # history
    years = list(range(date.today().year-10, date.today().year))

    sections = defaultdict(int)
    volumes = defaultdict(int)
    for section in sector.section_set.exclude(date__isnull=True):
        if section.date.year < min(years):
            years[:0] = list(range(section.date.year, min(years)))
        sections[section.date.year] += 1
        volumes[section.date.year] += section.volume

    sections_filled = [sections.get(y, 0) for y in years]
    p1 = figure(height=250, title="Total of done sections", toolbar_location=None, tools="")
    p1.vbar(x=years, top=sections_filled, width=0.9)
    p1.xgrid.grid_line_color = None
    p1.y_range.start = 0

    # planned
    descendent_sectors = sector.get_descendants(include_self=True)
    qs2 = Plot.objects.filter(sector__in=descendent_sectors, planned_next_section__gte=str(date.today()))
    years = list(range(date.today().year, date.today().year+10))
    sections = defaultdict(int)
    for plot in qs2.all():
        section_date = plot.planned_next_section
        if section_date.year > max(years):
            years.extend(list(range(max(years)+1, section_date.year+1)))
        sections[section_date.year] += 1

    sections_filled = [sections.get(y, 0) for y in years]
    p2 = figure(height=250, title="Total planned sections", toolbar_location=None, tools="")
    p2.vbar(x=years, top=sections_filled, width=0.9)
    p2.xgrid.grid_line_color = None
    p2.y_range.start = 0

    bokeh_script_1, bokeh_graph_1 = components(p1)
    bokeh_script_2, bokeh_graph_2 = components(p2)

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
            'bokeh_script_history': bokeh_script_1,
            'bokeh_graph_history': bokeh_graph_1,
            'bokeh_script_planned': bokeh_script_2,
            'bokeh_graph_planned': bokeh_graph_2
        },
    )


def map_view(request):
    plots_geojson = serialize(
        "geojson", Plot.objects.all(), geometry_field="geom", fields=("name",)
    )
    return render(
        request,
        "sylvis/map.html",
        {
            "plots_geojson": plots_geojson,
            # django-admin integration (stuff like side-menu, breadcrumbs...)
            # see https://github.com/django/django/blob/97e9a84d2746f76a635455c13bd512ea408755ac/django/contrib/admin/options.py#L1642-L1655
            **admin.site.each_context(request),
        },
    )
