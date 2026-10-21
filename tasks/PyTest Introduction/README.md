# PyTest Introduction Homework

## Install dependencies

Run these commands from the `PyTest Introduction` directory:

```powershell
python -m pip install -r requirements.txt
```

## Run tests

Run the full suite (including tests with marks):

```powershell
python -m pytest
```

Run tests assigned the `unmarked` mark:

```powershell
python -m pytest -m unmarked --html=reports/unmarked.html
```

Run CSV validation tests, excluding tests marked `xfail`:

```powershell
python -m pytest -m "validate_csv and not xfail" --html=reports/validate-csv.html
```

The default pytest configuration writes an HTML report to
`reports/pytest-report.html`. Each command above may supply a distinct
`--html` path to preserve a separate report for that run.

The CSV currently contains an invalid email address, a duplicate row, and a
record where `id=2` has `is_active=False`. The duplicate-row test is expected
to be xfailed; the email and `id=2` checks expose the data discrepancies as
test failures. The age check is intentionally skipped as requested.
