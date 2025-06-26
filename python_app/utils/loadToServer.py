import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import pyodbc

def write_df_to_sql(
    df: pd.DataFrame,
    table_name: str,
    database: str,
    server: str = 'localhost',
    driver: str = 'ODBC Driver 17 for SQL Server',
    if_exists: str = 'replace',
    trusted_connection: bool = True,
    username: str = None,
    password: str = None
) -> None:
    """
    Write a pandas DataFrame to a SQL Server table using SQLAlchemy with error handling.

    Parameters:
        df (pd.DataFrame): DataFrame to write.
        table_name (str): Name of the target SQL table.
        database (str): SQL Server database name.
        server (str): SQL Server host (default is 'localhost').
        driver (str): ODBC driver (default is 'ODBC Driver 17 for SQL Server').
        if_exists (str): What to do if table exists: 'fail', 'replace', or 'append'.
        trusted_connection (bool): Use Windows Authentication if True.
        username (str): SQL Server username (if using SQL auth).
        password (str): SQL Server password (if using SQL auth).
    """

    try:
        # Encode the connection string
        if trusted_connection:
            conn_str = f"mssql+pyodbc://@{server}/{database}?trusted_connection=yes&driver={driver}"
        else:
            if not username or not password:
                raise ValueError("Username and password must be provided for SQL authentication.")
            conn_str = f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}"

        # SQLAlchemy engine
        engine = create_engine(conn_str)

        # Write to SQL
        df.to_sql(table_name, con=engine, if_exists=if_exists, index=False)
        print(f"✅ Data written to table '{table_name}' successfully.")

    except SQLAlchemyError as e:
        print(f"❌ SQLAlchemy error while writing to '{table_name}': {e}")
    except ValueError as ve:
        print(f"❌ Value error: {ve}")
    except Exception as ex:
        print(f"❌ Unexpected error: {ex}")
