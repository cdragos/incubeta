import csv
from datetime import date
from decimal import Decimal

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from flights import models
from flights.constants import ROUTE_CSV_DATA_SAMPLES, ROUTE_CSV_HEADERS


@pytest.fixture
def csv_file(tmp_path):
    csv_file_path = tmp_path / "test_routes.csv"
    with open(csv_file_path, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=ROUTE_CSV_HEADERS)
        writer.writeheader()
        writer.writerows(ROUTE_CSV_DATA_SAMPLES)

    return csv_file_path


def assert_currencies():
    currencies = models.Currency.objects.all()
    assert len(currencies) == 2
    assert currencies[0].pk == "USD"
    assert currencies[1].pk == "DKK"


def assert_countries():
    countries = models.Country.objects.all()
    assert len(countries) == 4
    assert countries[0].iso_alpha2 == "TR"
    assert countries[0].name == "Turkey"
    assert countries[1].iso_alpha2 == "IR"
    assert countries[1].name == "Iran"
    assert countries[2].iso_alpha2 == "DK"
    assert countries[2].name == "Denmark"
    assert countries[3].iso_alpha2 == "KW"
    assert countries[3].name == "Kuwait"


def assert_cities():
    cities = models.City.objects.select_related("country").all()
    assert len(cities) == 4

    assert cities[0].name == "Ankara"
    assert cities[0].country.name == "Turkey"
    assert cities[1].name == "Tehran"
    assert cities[1].country.name == "Iran"
    assert cities[2].name == "Billund"
    assert cities[2].country.name == "Denmark"
    assert cities[3].name == "Kuwait"
    assert cities[3].country.name == "Kuwait"


def assert_stations():
    stations = models.Station.objects.all()
    assert len(stations) == 4
    assert stations[0].code == "ESB"
    assert stations[0].city.name == "Ankara"
    assert stations[1].code == "IKA"
    assert stations[1].city.name == "Tehran"
    assert stations[2].code == "BLL"
    assert stations[2].city.name == "Billund"
    assert stations[3].code == "KWI"
    assert stations[3].city.name == "Kuwait"


def assert_trip_details_first_set(route):
    route1_trip_details = route.trip_details.all()
    assert len(route1_trip_details) == 2

    route_trip_detail_1 = route1_trip_details[0]
    assert route_trip_detail_1.departure_date == date(2021, 11, 10)
    assert route_trip_detail_1.return_date is None
    assert route_trip_detail_1.fare_type == models.RouteTripDetail.FareTypes.ECONOMY
    assert route_trip_detail_1.trip_type == models.RouteTripDetail.TripTypes.ONEWAY
    assert (
        route_trip_detail_1.destination_url
        == "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=O&fromStation=ESB&toStation=IKA&departing=2021-11-10&bookingClass=E&adults=1&children=0&infants=0"
    )
    assert route_trip_detail_1.lowest_fare == Decimal("250")

    route_trip_detail_2 = route1_trip_details[1]
    assert route_trip_detail_2.departure_date == date(2021, 11, 10)
    assert route_trip_detail_2.return_date == date(2021, 11, 15)
    assert route_trip_detail_2.fare_type == models.RouteTripDetail.FareTypes.ECONOMY
    assert route_trip_detail_2.trip_type == models.RouteTripDetail.TripTypes.RETURN
    assert (
        route_trip_detail_2.destination_url
        == "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=R&fromStation=ESB&toStation=IKA&departing=2021-11-10&returning=2021-11-15&bookingClass=E&adults=1&children=0&infants=0"
    )
    assert route_trip_detail_2.lowest_fare == Decimal("444")


def assert_trip_details_second_set(route):
    route_trip_details = route.trip_details.all()
    assert len(route_trip_details) == 4

    route_trip_detail_1 = route_trip_details[0]
    assert route_trip_detail_1.departure_date == date(2022, 2, 21)
    assert route_trip_detail_1.return_date is None
    assert route_trip_detail_1.fare_type == models.RouteTripDetail.FareTypes.ECONOMY
    assert route_trip_detail_1.trip_type == models.RouteTripDetail.TripTypes.ONEWAY
    assert (
        route_trip_detail_1.destination_url
        == "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=O&fromStation=BLL&toStation=KWI&departing=2022-02-21&bookingClass=E&adults=1&children=0&infants=0"
    )
    assert route_trip_detail_1.lowest_fare == Decimal("3101")

    route_trip_detail_2 = route_trip_details[1]
    assert route_trip_detail_2.departure_date == date(2022, 3, 27)
    assert route_trip_detail_2.return_date == date(2022, 4, 1)
    assert route_trip_detail_2.fare_type == models.RouteTripDetail.FareTypes.ECONOMY
    assert route_trip_detail_2.trip_type == models.RouteTripDetail.TripTypes.RETURN
    assert (
        route_trip_detail_2.destination_url
        == "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=R&fromStation=BLL&toStation=KWI&departing=2022-03-27&returning=2022-04-01&bookingClass=E&adults=1&children=0&infants=0"
    )
    assert route_trip_detail_2.lowest_fare == Decimal("4560")

    route_trip_detail_3 = route_trip_details[2]
    assert route_trip_detail_3.departure_date == date(2021, 11, 11)
    assert route_trip_detail_3.return_date is None
    assert route_trip_detail_3.fare_type == models.RouteTripDetail.FareTypes.PREMIUM
    assert route_trip_detail_3.trip_type == models.RouteTripDetail.TripTypes.ONEWAY
    assert (
        route_trip_detail_2.destination_url
        == "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=R&fromStation=BLL&toStation=KWI&departing=2022-03-27&returning=2022-04-01&bookingClass=E&adults=1&children=0&infants=0"
    )
    assert route_trip_detail_3.lowest_fare == Decimal("11674")

    route_trip_detail_4 = route_trip_details[3]
    assert route_trip_detail_4.departure_date == date(2022, 3, 8)
    assert route_trip_detail_4.return_date == date(2022, 3, 14)
    assert route_trip_detail_4.fare_type == models.RouteTripDetail.FareTypes.PREMIUM
    assert route_trip_detail_4.trip_type == models.RouteTripDetail.TripTypes.RETURN
    assert (
        route_trip_detail_4.destination_url
        == "https://booking.qatarairways.com/nsp/views/showBooking.action?selLang=en&tripType=R&fromStation=BLL&toStation=KWI&departing=2022-03-08&returning=2022-03-14&bookingClass=B&adults=1&children=0&infants=0"
    )
    assert route_trip_detail_4.lowest_fare == Decimal("16430")


def test_sync_routes_data_command_file_does_not_exist():
    with pytest.raises(CommandError) as e:
        call_command("sync_routes_data", "non_existent_file.csv")
    assert "does not exist" in str(e.value)


def test_sync_routes_data_command_not_a_file(tmp_path):
    directory_path = tmp_path / "not_a_file"
    directory_path.mkdir()
    with pytest.raises(CommandError) as e:
        call_command("sync_routes_data", str(directory_path))
    assert "is not a file" in str(e.value)


def test_sync_routes_data_command_incorrect_suffix(tmp_path):
    incorrect_file = tmp_path / "test_routes.txt"
    incorrect_file.touch()
    with pytest.raises(CommandError) as e:
        call_command("sync_routes_data", str(incorrect_file))
    assert "is not a CSV file" in str(e.value)


@pytest.mark.django_db
def test_sync_routes_data_command_success(csv_file):
    call_command("sync_routes_data", str(csv_file))

    assert_currencies()
    assert_countries()
    assert_cities()
    assert_stations()

    routes = models.Route.objects.select_related(
        "currency",
        "destination_city",
        "destination_country",
        "destination_station",
        "origin_city",
        "origin_country",
        "origin_station",
    ).all()

    assert len(routes) == 2
    route_1 = routes[0]
    assert route_1.currency.code == "USD"
    assert route_1.destination_city.name == "Tehran"
    assert route_1.destination_country.name == "Iran"
    assert route_1.destination_station.code == "IKA"
    assert route_1.origin_city.name == "Ankara"
    assert route_1.origin_country.name == "Turkey"
    assert route_1.origin_station.code == "ESB"
    assert (
        route_1.destination_city_image_url
        == "https://www.qatarairways.com/content/dam/images/custom/FacebookRM/IKA.jpg?ver=2"
    )
    assert route_1.route_code == "ESB-IKA"

    assert_trip_details_first_set(route_1)

    route_2 = routes[1]
    assert route_2.currency.code == "DKK"
    assert route_2.destination_city.name == "Kuwait"
    assert route_2.destination_country.name == "Kuwait"
    assert route_2.destination_station.code == "KWI"
    assert route_2.origin_city.name == "Billund"
    assert route_2.origin_country.name == "Denmark"
    assert route_2.origin_station.code == "BLL"
    assert (
        route_2.destination_city_image_url
        == "https://www.qatarairways.com/content/dam/images/custom/FacebookRM/KWI.jpg?ver=2"
    )
    assert route_2.route_code == "BLL-KWI"

    assert_trip_details_second_set(route_2)
