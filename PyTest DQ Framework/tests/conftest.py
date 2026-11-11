import pytest

from src.connectors.postgres.postgres_connector import (
    PostgresConnectorContextManager
)
from src.connectors.file_system.parquet_reader import (
    ParquetReader
)
from src.data_quality.data_quality_validation_library import (
    DataQualityLibrary
)


def pytest_addoption(parser):

    parser.addoption("--db_host", action="store", default="localhost")
    parser.addoption("--db_port", action="store", default="5432")
    parser.addoption("--db_name", action="store")
    parser.addoption("--db_user", action="store")
    parser.addoption("--db_password", action="store")


def pytest_configure(config):

    required_options = [
        "db_name",
        "db_user",
        "db_password"
    ]

    for option in required_options:
        if not config.getoption(option):
            pytest.exit(
                f"Missing required option: --{option}"
            )


@pytest.fixture(scope="session")
def db_connection(request):

    with PostgresConnectorContextManager(
            db_host=request.config.getoption("db_host"),
            db_name=request.config.getoption("db_name"),
            db_port=request.config.getoption("db_port"),
            db_user=request
