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
            "facility_type",
            "visit_date",
            "avg_time_spent"
        ]
    )


@pytest.mark.parquet_data
@pytest.mark.uniqueness
def test_unique_facility_type_visit_date(
        target_data):

    duplicates = target_data.duplicated(
        subset=[
            "facility_type",
            "visit_date"
        ]
    ).sum()

    assert duplicates == 0


@pytest.mark.parquet_data
@pytest.mark.count
def test_row_count(
        source_data,
        target_data,
        data_quality_library):

    data_quality_library.check_count(
        source_data,
        target_data
    )


@pytest.mark.parquet_data
@pytest.mark.completeness
def test_data_completeness(
        source_data,
        target_data,
        data_quality_library):

    data_quality_library.check_data_full_data_set(
        source_data,
        target_data
    )
