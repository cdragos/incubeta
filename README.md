# Flight Search API

This is a Django-based Flight Search API that allows users to search for flight routes based on origin, destination, and departure date. The API provides endpoints to retrieve flight information and trip details.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Option 1: Running with UV](#option-1-running-with-uv)
  - [Option 2: Running with Docker](#option-2-running-with-docker)
- [Usage](#usage)
- [Testing](#testing)

## Prerequisites

Before running the Flight Search API, make sure you have the following prerequisites installed:

- Python 3.x
- pip (Python package installer)
- UV (if running with UV)
- Docker (if running with Docker)

## Installation

There are two options to run the Flight Search API: using UV or using Docker. Follow the instructions for your preferred method.

### Option 1: Running with UV

#### Install UV:

```shell
pip install uv
```

#### Create a virtual environment:

```shell
uv venv
source .venv/bin/activate
```

#### Compile the project dependencies:

```shell
uv pip compile pyproject.toml -o requirements.txt
uv pip compile pyproject.toml --extra testing -o requirements-dev.txt
```

#### Install the project dependencies:

```shell
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt
```

#### Run database migrations:

```shell
python manage.py migrate
```

### Option 2: Running with Docker

#### Build the Docker containers:

```shell
docker compose build
```

#### Start the Docker containers:

```shell
docker compose up -d
```

#### Access the web container:

```shell
docker compose exec web bash
```

#### Run database migrations:

```shell
docker compose exec web python manage.py migrate
```

## Usage
### Data Synchronization

To keep the flight route data up-to-date, we use a Django management command to import data from a CSV file. This can be executed as follows:

shell```
python manage.py sync_routes_data file_2.csv --batch-size=100
```

This command processes the CSV file in batches of 100 records at a time, ensuring efficient data handling and database performance.


## Testing

To run the test suite, use the following command:

```shell
pytest
```
