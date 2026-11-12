import pandas as pd

df = pd.read_parquet(
    "parquet_data/facility_type_avg_time_spent_per_visit_date",
    engine="pyarrow"
)

print(df.head())
print(df.columns)