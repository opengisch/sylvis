from django.shortcuts import get_object_or_404, render

from .models import Plot, Sector


def plot_view(request, plot_id):
    plot = get_object_or_404(Plot, id=plot_id)
    return render(request, "sylvis/aggregate_view.html", {"entity": plot})


def sector_view(request, sector_id):
    sector = get_object_or_404(Sector, id=sector_id)
    return render(request, "sylvis/aggregate_view.html", {"entity": sector})
