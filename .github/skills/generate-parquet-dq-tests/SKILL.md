name: generate-parquet-dq-tests description: >- Creates parquet dataset data quality test modules from docs/parquet-aggregated-data-mapping.md. Use this skill only after the PyTest DQ Framework has been implemented. Generates dataset-specific parquet validation tests and refuses framework, Jenkinsfile, connector, fixture, or conftest generation. disable-model-invocation: true
Generate Parquet DQ Tests
This skill is used during the PyTest DQ Framework assignment to generate parquet dataset validation tests from the mapping document.

Read first:

PyTest DQ Framework/docs/test-automation-strategy.md
docs/parquet-aggregated-data-mapping.md
Expected SQL must always be derived from the mapping document.

Do not copy SQL from data_dev/.

Do not embed framework code, Jenkins configuration, or connector code.

When this skill applies
Use this skill only when:

The PyTest DQ Framework has already been implemented.
Connectors, fixtures, conftest.py, pytest.ini, Jenkinsfile, and DataQualityLibrary already exist.
The target output location is:
tests/dq_checks/parquet_files/
A dataset exists in:
docs/parquet-aggregated-data-mapping.md
Refuse if:

The mapping document is unavailable.
The request is to generate framework components.
The request is to modify Jenkinsfile or conftest.py.
The request is to generate SQL from data_dev sources.
Inputs You Must Have
Required inputs:

Dataset definition from:
docs/parquet-aggregated-data-mapping.md
Existing DataQualityLibrary methods.
Existing parquet_reader fixture.
Existing db_connection fixture.
If mapping information is missing:

Stop test generation.
Report the missing mapping details.
Forbidden sources:

data_dev SQL
hardcoded expected results
parquet pipeline implementation code
Hard Rules
Generate test files only under:
tests/dq_checks/parquet_files/
Source data must come from PostgreSQL.

Target data must come from parquet files.

Expected SQL must be derived only from docs/parquet-aggregated-data-mapping.md.

Never embed dataset-specific SQL inside this skill document.

Never use SQL from data_dev.

Use DataQualityLibrary validation methods whenever available.

Every generated module must include:

Smoke validation
Count validation
Completeness validation
Uniqueness validation
Not-null validation
Use:

@pytest.mark.parquet_data
on every generated test.

Not-null checks must include all columns marked not-null in the mapping.

Uniqueness checks must use grouping columns defined by the mapping.

Do not create always-pass assertions.

Workflow
Read the dataset definition from the mapping document.
Determine source and target structures.
Derive expected SQL from transformation rules.
Identify not-null columns.
Identify grouping columns.
Build the parquet test module.
Add pytest markers.
Create smoke, count, completeness, uniqueness, and not-null tests.
Save the generated module under:
tests/dq_checks/parquet_files/
Validate naming and markers before completion.
Template
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
        COLUMN_LIST
    )


@pytest.mark.parquet_data
@pytest.mark.uniqueness
def test_uniqueness(
        target_data):

    duplicates = target_data.duplicated(
        subset=UNIQUE_COLUMNS
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
SQL Derivation (Generic)
Apply these generic rules:

Use joins defined by source relationships.
Convert timestamp columns to dates when required by the mapping.
Apply aggregation rules exactly as specified.
Apply GROUP BY to all grouping fields.
Construct derived fields exactly as described in the mapping.
Preserve aggregation logic from the mapping document.
Do not simplify SQL to force successful execution.
After Generation
Save the generated test file.
Ensure markers are correct.
Do not modify expected SQL to force passing results.
Run pytest only when explicitly requested.
Report failures as mapping, transformation, or parquet-data issues.
Skill Review (Self-Check Before Step 3)
Reject the skill if:

It contains expected SQL for specific datasets.
It instructs the use of data_dev SQL.
It omits completeness checks.
It omits count checks.
It omits uniqueness checks.
It omits not-null checks.
It swaps PostgreSQL and parquet sources.
It generates trivial assertions.
Any TODO remains.
