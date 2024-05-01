import csv
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation
from itertools import islice, product
from pathlib import Path
from typing import Any, Optional, Type
from urllib.parse import parse_qs, urlparse

from dateutil.parser import isoparse
from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import transaction
from django.db.models import Model

from flights import models

BATCH_SIZE = 100


class Command(BaseCommand):
    help = "Import routes data from a CSV file"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cache to store already fetched or created objects to avoid database hits.
        self.cache = {
            "currencies": {},
            "countries": {},
            "cities": {},
            "stations": {},
        }

    def add_arguments(self, parser: CommandParser) -> None:
        """Add command-line arguments to the parser."""
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")
        parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Number of records to process per batch")

    def handle(self, *args, **options) -> None:
        """Handle the command execution."""
        csv_file_path = options["csv_file"]
        batch_size = options["batch_size"]

        file_path = Path(csv_file_path)
        if not file_path.exists():
            raise CommandError(f"The file {csv_file_path} does not exist.")
        if not file_path.is_file():
            raise CommandError(f"The path {csv_file_path} is not a file.")
        if file_path.suffix != ".csv":
            raise CommandError(f"The file {csv_file_path} is not a CSV file.")

        self.import_routes_data(csv_file_path, batch_size)

    def import_routes_data(self, csv_file: str, batch_size: int) -> None:
        """Import routes data from the CSV file in batches."""
        self.stdout.write(f"Importing routes data from {csv_file}...")
        start_time = time.time()
        records_processed = 0

        with open(csv_file, "r") as file:
            reader = csv.DictReader(file)

            while True:
                batch = list(islice(reader, batch_size))
                if not batch:
                    break

                records_processed += len(batch)
                routes = self.process_batch(batch)
                with transaction.atomic():
                    # Bulk create to minimize database hits, handle conflicts to ensure idempotency.
                    routes = models.Route.objects.bulk_create(routes, ignore_conflicts=True)
                    # since I am using sqlite id's are not returned with the created objects
                    created_routes = models.Route.objects.filter(route_code__in=(route.route_code for route in routes))

                    route_trip_details = []
                    for route, row in zip(created_routes, batch):
                        route_trip_details.extend(self.create_route_trip_details(route, row))
                    models.RouteTripDetail.objects.bulk_create(route_trip_details, ignore_conflicts=True)

        end_time = time.time()
        total_duration = end_time - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed in {total_duration:.2f} seconds. Records processed {records_processed}."
            )
        )

    def process_batch(self, batch) -> list[models.Route]:
        """Process a batch of CSV rows and create Route instances."""
        routes = []
        for row in batch:
            currency = self.cache_lookup_or_create(
                key=row["currency_code"],
                cache_key="currencies",
                model=models.Currency,
                params={"code": row["currency_code"]},
            )
            origin_country = self.cache_lookup_or_create(
                key=row["org_country_code"],
                cache_key="countries",
                model=models.Country,
                params={
                    "iso_alpha2": row["org_country_code"],
                    "defaults": {"name": row["org_country_name"]},
                },
            )
            origin_city = self.cache_lookup_or_create(
                key=row["org_city_name"],
                cache_key="cities",
                model=models.City,
                params={"name": row["org_city_name"], "country": origin_country},
            )
            origin_station = self.cache_lookup_or_create(
                key=row["org_station_code"],
                cache_key="stations",
                model=models.Station,
                params={"code": row["org_station_code"], "city": origin_city},
            )
            destination_country = self.cache_lookup_or_create(
                key=row["dst_country_code"],
                cache_key="countries",
                model=models.Country,
                params={
                    "iso_alpha2": row["dst_country_code"],
                    "defaults": {"name": row["dst_country_name"]},
                },
            )
            destination_city = self.cache_lookup_or_create(
                key=row["dst_city_name"],
                cache_key="cities",
                model=models.City,
                params={"name": row["dst_city_name"], "country": destination_country},
            )
            destination_station = self.cache_lookup_or_create(
                key=row["dst_station_code"],
                cache_key="stations",
                model=models.Station,
                params={"code": row["dst_station_code"], "city": destination_city},
            )
            route = models.Route(
                route_code=row["route"],
                currency=currency,
                origin_country=origin_country,
                origin_city=origin_city,
                origin_station=origin_station,
                destination_country=destination_country,
                destination_city=destination_city,
                destination_station=destination_station,
                destination_city_image_url=row["destination_city_image_url"],
            )
            routes.append(route)

        return routes

    def create_route_trip_details(self, route: models.Route, row: dict[str, str]) -> list[models.RouteTripDetail]:
        """Create RouteTripDetail instances for a given Route and CSV row."""
        route_trip_details = []
        for fare_type, trip_type in product(
            models.RouteTripDetail.FareTypes.values, models.RouteTripDetail.TripTypes.values
        ):
            # Compose the URL and fare field names dynamically based on fare and trip types.
            destination_url_field = f"destination_url_{fare_type}_{trip_type}"
            lowest_fare_field = f"lowest_fare_{fare_type}_{trip_type}"

            destination_url = row[destination_url_field]
            if not destination_url:
                continue

            lowest_fare = self.parse_decimal(row[lowest_fare_field])
            departure_date, return_date = self.extract_dates(destination_url)
            if not departure_date:
                continue

            route_trip_detail = models.RouteTripDetail(
                route=route,
                departure_date=departure_date,
                return_date=return_date,
                fare_type=fare_type,
                trip_type=trip_type,
                destination_url=destination_url,
                lowest_fare=lowest_fare,
            )
            route_trip_details.append(route_trip_detail)
        return route_trip_details

    def extract_dates(self, url: str) -> tuple[Optional[datetime], Optional[datetime]]:
        """Extract departure and return dates from the URL."""
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        departing = query_params.get("departing", [None])[0]
        departure_date = isoparse(departing) if departing else None

        returning = query_params.get("returning", [None])[0]
        return_date = isoparse(returning) if returning else None

        return departure_date, return_date

    def cache_lookup_or_create(self, key: str, cache_key: str, model: Type[Model], params: dict[str, Any]) -> Model:
        """Look up an object in the cache or create it if it doesn't exist."""
        if key in self.cache[cache_key]:
            return self.cache[cache_key][key]
        else:
            obj, _ = model.objects.get_or_create(**params)
            self.cache[cache_key][key] = obj
            return obj

    def parse_decimal(self, value: str) -> Optional[Decimal]:
        try:
            return Decimal(float(value))
        except (InvalidOperation, TypeError, ValueError, TypeError):
            return None
