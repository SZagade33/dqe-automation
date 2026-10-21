from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(scope="session")
def path_to_file():
    return Path(__file__).resolve().parents[1] / "src" / "data" / "data.csv"


@pytest.fixture(scope="session")
def read_csv(path_to_file):
    return pd.read_csv(path_to_file)


@pytest.fixture(scope="session")
def actual_schema(read_csv):
    return read_csv.columns.tolist()


@pytest.fixture(scope="session")
def expected_schema():
    return ["id", "name", "age", "email", "is_active"]


@pytest.fixture(scope="session")
def validate_schema(actual_schema, expected_schema):
    assert actual_schema == expected_schema, (
        f"CSV schema mismatch: expected {expected_schema}, got {actual_schema}"
    )
    return True


def pytest_collection_modifyitems(items):
    for item in items:
        if not item.own_markers:
            item.add_marker(pytest.mark.unmarked)
