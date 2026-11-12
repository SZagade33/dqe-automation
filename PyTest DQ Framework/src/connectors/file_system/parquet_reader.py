from pathlib import Path

import pandas as pd


class ParquetReader:

    def process(
            self,
            path,
            include_subfolders=True):

        parquet_files = []

        if include_subfolders:
            parquet_files = list(
                Path(path).rglob("*.parquet")
            )
        else:
            parquet_files = list(
                Path(path).glob("*.parquet")
            )

        if not parquet_files:
            raise FileNotFoundError(
                f"No parquet files found in {path}"
            )

        dataframes = [
            pd.read_parquet(file)
            for file in parquet_files
        ]

        return pd.concat(
            dataframes,
            ignore_index=True
        )
