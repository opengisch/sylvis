from collections import defaultdict
from datetime import date

from bokeh.embed import components
from bokeh.models import LinearAxis, Range1d
from bokeh.models.tickers import FixedTicker
from bokeh.plotting import figure
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.serializers import serialize
from django.db.models import Max
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from .forms import AddInventoryForm, AddSectionForm, AddTreatmentForm
from .models import Plot, Sector


@login_required
def home(request):
    return render(request, "sylvis/home.html")


@login_required
def plot_view(request, plot_id):
    plot = get_object_or_404(Plot, id=plot_id)

    section_form = AddSectionForm(plot_id)
    inventory_form = AddInventoryForm(plot_id)
    treatment_form = AddTreatmentForm(plot_id)

    if request.method == "POST":
        if "add_section" in request.POST:
            section_form = AddSectionForm(plot_id, request.POST)
            if section_form.is_valid():
                section_form.save()
                return HttpResponseRedirect(request.path_info)

        if "add_inventory" in request.POST:
            inventory_form = AddInventoryForm(plot_id, request.POST)
            if inventory_form.is_valid():
                inventory_form.save()
                return HttpResponseRedirect(request.path_info)

        if "add_treatment" in request.POST:
            treatment_form = AddTreatmentForm(plot_id, request.POST)
            if treatment_form.is_valid():
                treatment_form.save()
                return HttpResponseRedirect(request.path_info)

    return render(
        request,
        "sylvis/detail_plot.html",
        {
            "entity": plot,
            "features_geojson": serialize("geojson", [plot], geometry_field="geom"),
            "section_form": section_form,
            "inventory_form": inventory_form,
            "treatment_form": treatment_form,
        },
    )


@login_required
def sector_view(request, sector_id):
    sector = get_object_or_404(Sector, id=sector_id)

    # history
    years = list(range(date.today().year - 10, date.today().year))

    sections = defaultdict(int)
    volumes = defaultdict(int)
    for section in sector.section_set.exclude(date__isnull=True):
        if section.date.year < min(years):
            years[:0] = list(range(section.date.year, min(years)))
        sections[section.date.year] += 1
        volumes[section.date.year] += section.volume

    sections_filled = [sections.get(y, 0) for y in years]
    volumes_filled = [volumes.get(y, 0) for y in years]

    p1 = figure(
        y_range=(0, max(sections_filled) + 1),
        height=250,
        title="Total of done sections",
        toolbar_location=None,
        tools="",
    )
    p1.xaxis.axis_label = "Year"
    p1.yaxis.axis_label = "Sections"
    p1.xaxis.ticker = FixedTicker(ticks=years)
    p1.xgrid.grid_line_color = None

    p1.line(x=years, y=sections_filled, line_width=0.9, line_color="#3c9765")
    p1.circle(x=years, y=sections_filled, radius=0.1, fill_color="#4db164")

    # Setting the second y axis range name and range
    p1.extra_y_ranges = {"foo": Range1d(start=0, end=1.1 * float(max(volumes_filled)))}
    # Adding the second axis to the plot.
    p1.add_layout(LinearAxis(y_range_name="foo", axis_label="Volumes"), "right")

    p1.vbar(
        x=years,
        top=volumes_filled,
        width=0.9,
        fill_color="#4db164",
        line_color="#3c9765",
        fill_alpha=0.5,
        y_range_name="foo",
    )
    p1.sizing_mode = "scale_both"

    # planned
    descendent_sectors = sector.get_descendants(include_self=True)
    qs2 = Plot.objects.filter(
        sector__in=descendent_sectors, planned_next_section__gte=str(date.today())
    )
    years = list(range(date.today().year, date.today().year + 10))
    sections = defaultdict(int)
    for plot in qs2.all():
        section_date = plot.planned_next_section
        if section_date.year > max(years):
            years.extend(list(range(max(years) + 1, section_date.year + 1)))
        sections[section_date.year] += 1

    sections_filled = [sections.get(y, 0) for y in years]

    p2 = figure(
        height=250, title="Total planned sections", toolbar_location=None, tools=""
    )
    p2.xaxis.axis_label = "Year"
    p2.yaxis.axis_label = "Sections"
    p2.xaxis.ticker = FixedTicker(ticks=years)
    p2.xgrid.grid_line_color = None

    p2.line(x=years, y=sections_filled, line_width=0.9, line_color="#3c9765")
    p2.circle(x=years, y=sections_filled, radius=0.1, fill_color="#4db164")
    p2.y_range.start = 0
    p2.sizing_mode = "scale_both"

    bokeh_script_1, bokeh_graph_1 = components(p1)
    bokeh_script_2, bokeh_graph_2 = components(p2)

    return render(
        request,
        "sylvis/detail_sector.html",
        {
            "entity": sector,
            "features_geojson": serialize(
                "geojson", [sector], geometry_field="computed_geom"
            ),
            "bokeh_script_history": bokeh_script_1,
            "bokeh_graph_history": bokeh_graph_1,
            "bokeh_script_planned": bokeh_script_2,
            "bokeh_graph_planned": bokeh_graph_2,
        },
    )


@login_required
@cache_page(60 * 15)
def map_view(request):
    plots = Plot.objects.all()
    plots_geojson = serialize(
        "geojson",
        plots,
        geometry_field="geom",
        fields=("pk", "name"),
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
            fields=("pk", "name", "level"),
        )
        sectors_geojsons.append(sectors_geojson)

    return render(
        request,
        "sylvis/map.html",
        {
            "plots_geojson": plots_geojson,
            "sectors_geojsons": f"[{','.join(sectors_geojsons)}]",
        },
    )


@receiver(post_save, sender=Plot)
@receiver(post_save, sender=Sector)
@receiver(post_delete, sender=Plot)
@receiver(post_delete, sender=Sector)
def delete_cache(sender, **kwargs):
    cache.clear()
