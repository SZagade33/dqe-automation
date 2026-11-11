import pandas as pd
import psycopg2


class PostgresConnectorContextManager:

    def __init__(
            self,
            db_host,
            db_name,
            db_port,
            db_user,
            db_password):

        self.connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            port=db_port,
            user=db_user,
            password=db_password
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def get_data_sql(self, query):
        return pd.read_sql(query, self.connection)
