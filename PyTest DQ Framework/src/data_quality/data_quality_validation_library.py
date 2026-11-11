import pandas as pd


class DataQualityLibrary:
    """
    Data Quality Validation Library
    """

    @staticmethod
    def check_duplicates(df, column_names=None):

        if column_names:
            duplicates = df.duplicated(subset=column_names).sum()
        else:
            duplicates = df.duplicated().sum()

        assert duplicates == 0, (
            f"Found {duplicates} duplicate records"
        )

    @staticmethod
    def check_count(df1, df2):

        assert len(df1) == len(df2), (
            f"Count mismatch. "
            f"Source={len(df1)}, Target={len(df2)}"
        )

    @staticmethod
    def check_data_full_data_set(df1, df2):

        pd.testing.assert_frame_equal(
            df1.reset_index(drop=True),
            df2.reset_index(drop=True),
            check_dtype=False
        )

    @staticmethod
    def check_dataset_is_not_empty(df):

        assert not df.empty, (
            "Dataset is empty"
        )

    @staticmethod
    def check_not_null_values(df, column_names=None):

        if column_names is None:
            column_names = df.columns

        for col in column_names:

            null_count = df[col].isnull().sum()

            assert null_count == 0, (
                f"Column '{col}' contains "
                f"{null_count} NULL values"
            )
