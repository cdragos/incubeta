from decimal import Decimal

import pytest

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
