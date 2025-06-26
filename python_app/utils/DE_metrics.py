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

def get_num_unique_authors(api_df: pd.DataFrame) -> int:
    """Return the number of unique authors."""
    if "Author" in api_df.columns:
        return api_df["Author"].nunique()
    return 0

def get_most_borrowed_book(books_df: pd.DataFrame) -> str:
    """Return the most borrowed book."""
    if "Books" in books_df.columns:
        return books_df["Books"].mode().iloc[0]
    return ""

def get_most_active_customer(books_df: pd.DataFrame) -> str:
    """Return the most active customer."""
    if "Customer ID" in books_df.columns:
        return str(books_df["Customer ID"].mode().iloc[0])
    return ""

def get_average_borrow_duration(books_df: pd.DataFrame) -> float:
    """Return the average borrow duration."""
    if "BorrowDuration" in books_df.columns:
        return books_df["BorrowDuration"].mean()
    return 0.0

def get_num_overdue(books_df: pd.DataFrame) -> int:
    """Return the number of overdue returns."""
    if "OverdueAlert" in books_df.columns:
        return (books_df["OverdueAlert"] == "OVERDUE").sum()
    return 0

def get_num_currently_borrowed(books_df: pd.DataFrame) -> int:
    """Return the number of books currently borrowed."""
    if "Book Returned" in books_df.columns:
        return books_df["Book Returned"].isna().sum()
    return 0
