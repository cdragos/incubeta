import pytest
from django.core.management.base import CommandError
from django.core.management import call_command


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
