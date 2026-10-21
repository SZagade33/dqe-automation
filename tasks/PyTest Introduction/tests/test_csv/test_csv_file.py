import re

import pytest


def test_file_not_empty(read_csv):
    assert not read_csv.empty, "The CSV file must contain at least one data row."


@pytest.mark.validate_csv
def test_validate_schema(validate_schema):
    assert validate_schema, "The CSV columns must match the expected schema."


@pytest.mark.validate_csv
@pytest.mark.skip(reason="Age validation is intentionally skipped for this assignment.")
def test_age_column_valid(read_csv):
    valid_ages = read_csv["age"].between(0, 100)
    assert valid_ages.all(), (
        f"Age values must be between 0 and 100; invalid values: "
        f"{read_csv.loc[~valid_ages, 'age'].tolist()}"
    )


@pytest.mark.validate_csv
def test_email_column_valid(read_csv):
    email_pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    valid_emails = read_csv["email"].fillna("").map(
        lambda email: bool(email_pattern.fullmatch(email))
    )
    assert valid_emails.all(), (
        f"Invalid email address(es): "
        f"{read_csv.loc[~valid_emails, 'email'].tolist()}"
    )


@pytest.mark.validate_csv
@pytest.mark.xfail(reason="The CSV intentionally contains a duplicate row.")
def test_duplicates(read_csv):
    duplicate_rows = read_csv[read_csv.duplicated(keep=False)]
    assert duplicate_rows.empty, (
        f"Duplicate CSV rows found: {duplicate_rows.to_dict(orient='records')}"
    )


@pytest.mark.validate_csv
@pytest.mark.parametrize("player_id, expected_active", [(1, False), (2, True)])
def test_active_players(read_csv, player_id, expected_active):
    actual_values = read_csv.loc[
        read_csv["id"] == player_id, "is_active"
    ].tolist()
    assert len(actual_values) == 1, (
        f"Expected exactly one CSV row for id={player_id}; found {len(actual_values)}."
    )
    assert actual_values[0] == expected_active, (
        f"Expected is_active={expected_active} for id={player_id}, "
        f"got {actual_values[0]}."
    )


def test_active_player(read_csv):
    player_id = 2
    expected_active = True
    actual_values = read_csv.loc[
        read_csv["id"] == player_id, "is_active"
    ].tolist()
    assert len(actual_values) == 1, (
        f"Expected exactly one CSV row for id={player_id}; found {len(actual_values)}."
    )
    assert actual_values[0] == expected_active, (
        f"Expected is_active={expected_active} for id={player_id}, "
        f"got {actual_values[0]}."
    )
