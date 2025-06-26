import pandas as pd

def get_num_customers(customers_df: pd.DataFrame) -> int:
    """Return the number of unique customers."""
    if "Customer ID" in customers_df.columns:
        return customers_df["Customer ID"].nunique()
    return 0

def get_num_books(books_df: pd.DataFrame) -> int:
    """Return the number of unique books."""
    if "Books" in books_df.columns:
        return books_df["Books"].nunique()
    return 0

def get_num_api_requests(api_df: pd.DataFrame) -> int:
    """Return the number of API requests (rows in API-enriched DataFrame)."""
    return len(api_df)
