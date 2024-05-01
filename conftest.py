import pytest


@pytest.fixture(autouse=True)
def use_sqlite_memory_database(settings):
    settings.DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
