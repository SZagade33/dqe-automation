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

    parser.addoption(
        "--db_host",
        action="store",
        default="localhost"
    )

    parser.addoption(
        "--db_port",
        action="store",
        default="5432"
    )

    parser.addoption(
        "--db_name",
        action="store",
        default="postgres"
    )

    parser.addoption(
        "--db_user",
        action="store",
        default="postgres"
    )

    parser.addoption(
        "--db_password",
        action="store",
        default="postgres"
    )


def pytest_configure(config):

    config.addinivalue_line(
        "markers",
        "parquet_data: parquet dataset tests"
    )

    config.addinivalue_line(
        "markers",
        "smoke: smoke tests"
    )

    config.addinivalue_line(
        "markers",
        "count: count validation tests"
    )

    config.addinivalue_line(
        "markers",
        "completeness: completeness validation tests"
    )

    config.addinivalue_line(
        "markers",
        "uniqueness: uniqueness validation tests"
    )

    config.addinivalue_line(
        "markers",
        "not_null: not null validation tests"
    )


@pytest.fixture(scope="session")
def db_connection(request):

    with PostgresConnectorContextManager(
            db_host=request.config.getoption("db_host"),
            db_name=request.config.getoption("db_name"),
            db_port=request.config.getoption("db_port"),
            db_user=request.config.getoption("db_user"),
            db_password=request.config.getoption("db_password")
    ) as connector:

        yield connector


@pytest.fixture(scope="session")
def parquet_reader():

    return ParquetReader()


@pytest.fixture(scope="session")
def data_quality_library():

    return DataQualityLibrary()
