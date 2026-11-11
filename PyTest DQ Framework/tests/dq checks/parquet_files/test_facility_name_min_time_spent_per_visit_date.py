import pytest


@pytest.mark.parquet_data
@pytest.mark.smoke
def test_dataset_not_empty(
        target_data,
        data_quality_library):

    data_quality_library.check_dataset_is_not_empty(
        target_data
    )


@pytest.mark.parquet_data
@pytest.mark.not_null
def test_not_null_columns(
        target_data,
        data_quality_library):

    data_quality_library.check_not_null_values(
        target_data,
        [
            "facility_name",
            "visit_date",
            "min_time_spent"
        ]
    )


@pytest.mark.parquet_data
@pytest.mark.uniqueness
def test_unique_facility_name_visit_date(
        target_data):

    duplicates = target_data.duplicated(
        subset=[
            "facility_name",
            "visit_date"
        ]
    ).sum()

    assert duplicates == 0
