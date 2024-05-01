from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import HttpRequest, JsonResponse
from http import HTTPStatus
from .forms import FlightSearchForm
from django.db.models import Q
from .models import Route


@require_GET
def flight_search_view(request: HttpRequest) -> JsonResponse:
    form = FlightSearchForm(request.GET)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=HTTPStatus.BAD_REQUEST)

    origin = form.cleaned_data["origin"].lower().strip()
    destination = form.cleaned_data["destination"].lower().strip()
    departure_date = form.cleaned_data["departure_date"]

    routes = (
        Route.objects.select_related(
            "origin_city",
            "origin_country",
            "origin_station",
            "destination_city",
            "destination_country",
            "destination_station",
        )
        .filter(
            Q(origin_city__name__iexact=origin)
            | Q(origin_station__code__iexact=origin)
            | Q(origin_country__iso_alpha2__iexact=origin)
            | Q(origin_country__name__iexact=origin),
            Q(destination_city__name__iexact=destination)
            | Q(destination_station__code__iexact=destination)
            | Q(destination_country__iso_alpha2__iexact=destination)
            | Q(destination_country__name__iexact=destination),
        )
    )

    return JsonResponse({"results": []})
