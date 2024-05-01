from decimal import Decimal
from http import HTTPStatus

import pytest
from django.urls import reverse

from flights import models


@pytest.fixture
def create_route():
    def _create_route(
        route_code,
        origin_country_name="United States",
        origin_country_code="US",
        destination_country_name="Germany",
        destination_country_code="DE",
        origin_city_name="Los Angeles",
        destination_city_name="Berlin",
        origin_station_code="NYC",
        destination_station_code="BER",
        **kwargs,
    ):
        # Create or get currency, countries, cities, and stations if needed
        currency, _ = models.Currency.objects.get_or_create(code="USD")
        origin_country, _ = models.Country.objects.get_or_create(
            iso_alpha2=origin_country_code, name=origin_country_name
        )
        destination_country, _ = models.Country.objects.get_or_create(
            iso_alpha2=destination_country_code, name=destination_country_name
        )
        origin_city, _ = models.City.objects.get_or_create(name=origin_city_name, country=origin_country)
        destination_city, _ = models.City.objects.get_or_create(name=destination_city_name, country=destination_country)
        origin_station, _ = models.Station.objects.get_or_create(code=origin_station_code, city=origin_city)
        destination_station, _ = models.Station.objects.get_or_create(
            code=destination_station_code, city=destination_city
        )

        # Create the route
        route = models.Route.objects.create(
            route_code=route_code,
            currency=currency,
            origin_city=origin_city,
            destination_city=destination_city,
            origin_country=origin_country,
            destination_country=destination_country,
            origin_station=origin_station,
            destination_station=destination_station,
            **kwargs,
        )
        return route

    return _create_route


@pytest.fixture
def create_trip_detail(create_route):
    def _create_trip_detail(
        route,
        departure_date,
        fare_type=models.RouteTripDetail.FareTypes.ECONOMY,
        trip_type=models.RouteTripDetail.TripTypes.ONEWAY,
        return_date=None,
        destination_url="",
        lowest_fare=None,
        **kwargs,
    ):
        trip_detail = models.RouteTripDetail.objects.create(
            route=route,
            departure_date=departure_date,
            return_date=return_date,
            fare_type=fare_type,
            trip_type=trip_type,
            destination_url=destination_url,
            lowest_fare=lowest_fare,
        )
        return trip_detail

    return _create_trip_detail


@pytest.mark.django_db
def test_flight_search_view_filters(client, create_route, create_trip_detail):
    create_route(route_code="LAX-BER")
    route_2 = create_route(
        route_code="NYC-FRA",
        origin_country_name="United States",
        origin_country_code="US",
        destination_country_name="Germany",
        destination_country_code="DE",
        origin_city_name="New York",
        destination_city_name="Frankfurt",
        origin_station_code="JFK",
        destination_station_code="FRA",
    )
    create_trip_detail(route=route_2, departure_date="2023-10-05", lowest_fare=Decimal("10"))
    create_trip_detail(
        route=route_2,
        departure_date="2023-10-05",
        fare_type=models.RouteTripDetail.FareTypes.PREMIUM,
        trip_type=models.RouteTripDetail.TripTypes.ONEWAY,
        lowest_fare=Decimal("20"),
    )

    # URL for the flight search view
    url = reverse("flight_search")

    # Test filtering by origin city name, destination city name and valid departure date
    response = client.get(url, {"origin": "New York", "destination": "Frankfurt", "departure_date": "2023-10-05"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    results = data["results"]

    assert len(results) == 1
    assert results[0] == {
        "code": "NYC-FRA",
        "destination_city": "Frankfurt",
        "destination_country": "Germany",
        "destination_station": "FRA",
        "origin_city": "New York",
        "origin_station": "JFK",
        "trip_details": [
            {
                "departure_date": "2023-10-05",
                "destination_url": "",
                "fare_type": "economy",
                "lowest_fare": "10.00",
                "return_date": None,
                "trip_type": "oneway",
            },
            {
                "departure_date": "2023-10-05",
                "destination_url": "",
                "fare_type": "premium",
                "lowest_fare": "20.00",
                "return_date": None,
                "trip_type": "oneway",
            },
        ],
    }

    # Test filtering by origin city name, destination city name and invalid departure date
    response = client.get(url, {"origin": "New York", "destination": "Frankfurt", "departure_date": "2023-11-05"})
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data == {"results": []}
