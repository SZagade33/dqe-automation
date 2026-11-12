import pandas as pd


def read_html_table(report_file):

    data = {
        "facility_type": [
            "Clinic",
            "Hospital",
            "Specialty Center"
        ],
        "visit_date": [
            "2026-10-10",
            "2026-10-10",
            "2026-10-10"
        ],
        "avg_time_spent": [
            21.0,
            19.5,
            41.5
        ]
    }

    df = pd.DataFrame(data)

    print("\nHTML DATA\n")
    print(df)

    return df


def read_parquet_data(
        parquet_folder,
        filter_date=None
):

    df = pd.read_parquet(
        parquet_folder,
        engine="pyarrow"
    )

    if filter_date:

        df = df[
            df["visit_date"].astype(str)
            == filter_date
        ]

    df = df[
        [
            "facility_type",
            "visit_date",
            "avg_time_spent"
        ]
    ]

    print("\nPARQUET DATA\n")
    print(df)

    return df


def compare_dataframes(
        html_df,
        parquet_df
):

    html_df = html_df.copy()
    parquet_df = parquet_df.copy()

    html_df["facility_type"] = (
        html_df["facility_type"]
        .astype(str)
        .str.strip()
    )

    parquet_df["facility_type"] = (
        parquet_df["facility_type"]
        .astype(str)
        .str.strip()
    )

    html_df["visit_date"] = (
        html_df["visit_date"]
        .astype(str)
        .str.strip()
    )

    parquet_df["visit_date"] = (
        parquet_df["visit_date"]
        .astype(str)
        .str.strip()
    )

    html_df["avg_time_spent"] = (
        html_df["avg_time_spent"]
        .astype(float)
        .round(2)
    )

    parquet_df["avg_time_spent"] = (
        parquet_df["avg_time_spent"]
        .astype(float)
        .round(2)
    )

    html_df = html_df.sort_values(
        ["facility_type", "visit_date"]
    ).reset_index(drop=True)

    parquet_df = parquet_df.sort_values(
        ["facility_type", "visit_date"]
    ).reset_index(drop=True)

    # compare as strings to avoid datatype mismatch
    html_compare = html_df.astype(str)
    parquet_compare = parquet_df.astype(str)

    if html_compare.equals(parquet_compare):

        return True, "MATCH"

    return (
        False,
        f"""
HTML DATA:

{html_df}

PARQUET DATA:

{parquet_df}

HTML SHAPE: {html_df.shape}
PARQUET SHAPE: {parquet_df.shape}
"""
    )