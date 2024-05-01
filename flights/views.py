from http import HTTPStatus

from django.db.models import Exists, OuterRef, Prefetch, Q
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_GET

from .forms import FlightSearchForm
from .models import Route, RouteTripDetail


@require_GET
def flight_search_view(request: HttpRequest) -> JsonResponse:
    form = FlightSearchForm(request.GET)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=HTTPStatus.BAD_REQUEST)

    origin = form.cleaned_data["origin"].lower().strip()
    destination = form.cleaned_data["destination"].lower().strip()
    departure_date = form.cleaned_data["departure_date"]

    # Create a subquery for RouteTripDetail that matches the departure date
    trip_details_subquery = RouteTripDetail.objects.filter(route=OuterRef("pk"), departure_date=departure_date)

    # Use Prefetch to optimize loading of related trip details
    trip_details_prefetch = Prefetch(
        "trip_details",
        queryset=RouteTripDetail.objects.filter(departure_date=departure_date),
    )

    routes = (
        Route.objects.select_related(
            "origin_city",
            "origin_country",
            "origin_station",
            "destination_city",
            "destination_country",
            "destination_station",
        )
        .prefetch_related(trip_details_prefetch)
        .filter(
            Q(origin_city__name__iexact=origin)
            | Q(origin_station__code__iexact=origin)
            | Q(origin_country__iso_alpha2__iexact=origin)
            | Q(origin_country__name__iexact=origin),
            Q(destination_city__name__iexact=destination)
            | Q(destination_station__code__iexact=destination)
            | Q(destination_country__iso_alpha2__iexact=destination)
            | Q(destination_country__name__iexact=destination),
            Exists(trip_details_subquery),
        )
    )
    results = []
    for route in routes:
        trip_details = [
            {
                "departure_date": trip.departure_date,
                "return_date": trip.return_date,
                "fare_type": trip.fare_type,
                "trip_type": trip.trip_type,
                "destination_url": trip.destination_url,
                "lowest_fare": trip.lowest_fare,
            }
            for trip in route.trip_details.all()
        ]
        route_dict = {
            "code": route.route_code,
            "origin_city": route.origin_city.name,
            "origin_station": route.origin_station.code,
            "destination_city": route.destination_city.name,
            "destination_country": route.destination_country.name,
            "destination_station": route.destination_station.code,
            "trip_details": trip_details,
        }
        results.append(route_dict)

    # in production code I would choose to use Django Rest Framework
    # and use serializers to return serialized data, but for simplicity I choose bare django approach
    return JsonResponse({"results": results})
