from pathlib import Path
from django.core.management.base import BaseCommand, CommandParser, CommandError
import time


BATCH_SIZE = 100


class Command(BaseCommand):
    help = "Import routes data from a CSV file"

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

        end_time = time.time()
        total_duration = end_time - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed in {total_duration:.2f} seconds. Records processed {records_processed}."
            )
        )
