from django.contrib import admin
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
