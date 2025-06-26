import pandas as pd
from datetime import datetime

# Function to read a CSV file
def read_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

# Function to clean data by dropping rows where all values are NaN
def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna(how='all')

# Function to drop duplicate rows in a dataframe
def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()

# Function to clean and correct invalid date formats in a column
def correct_dates(df: pd.DataFrame, column_name: str, default_date: str = '01/01/2023') -> pd.DataFrame:
    df[column_name] = df[column_name].astype(str).str.replace('"', '', regex=False)
    df[column_name] = df[column_name].apply(
        lambda x: x if len(x.split('/')) == 3 and x.split('/')[0].isdigit() and int(x.split('/')[0]) <= 31 else default_date
    )
    df[column_name] = pd.to_datetime(df[column_name], dayfirst=True, errors='coerce')
    return df

# Function to save a cleaned dataframe to a CSV file
def save_to_csv(df: pd.DataFrame, output_file: str) -> None:
    df.to_csv(output_file, index=False)

def fix_swapped_dates(df: pd.DataFrame, checkout_col: str = 'Book checkout', returned_col: str = 'Book Returned') -> pd.DataFrame:

    #Ensures 'Book checkout' is earlier than 'Book Returned'.
    #If not, it swaps them.

    # Convert to datetime just in case they aren't already
    df[checkout_col] = pd.to_datetime(df[checkout_col], errors='coerce')
    df[returned_col] = pd.to_datetime(df[returned_col], errors='coerce')

    # Find rows where checkout date is after returned date
    mask = df[checkout_col] > df[returned_col]

    # Swap the dates for those rows
    df.loc[mask, [checkout_col, returned_col]] = df.loc[mask, [returned_col, checkout_col]].values

    return df

def fix_swapped_and_future_dates(
    df: pd.DataFrame,
    checkout_col: str = 'Book checkout',
    returned_col: str = 'Book Returned',
    max_year_diff: int = 5
) -> pd.DataFrame:
    """
    Ensures checkout is before return date.
    If not, swaps them.
    Also corrects return dates that are more than `max_year_diff` years after checkout.
    """
    # Convert to datetime
    df[checkout_col] = pd.to_datetime(df[checkout_col], errors='coerce')
    df[returned_col] = pd.to_datetime(df[returned_col], errors='coerce')

    # Step 1: Swap if checkout > returned
    mask_swapped = df[checkout_col] > df[returned_col]
    df.loc[mask_swapped, [checkout_col, returned_col]] = df.loc[mask_swapped, [returned_col, checkout_col]].values

    # Step 2: Fix if return year is too far in future relative to checkout
    mask_future = (df[returned_col].dt.year - df[checkout_col].dt.year) > max_year_diff

    def correct_year(row):
        checkout_date = row[checkout_col]
        returned_date = row[returned_col]
        # Set returned date to the same year as checkout
        if pd.notna(returned_date) and pd.notna(checkout_date):
            return returned_date.replace(year=checkout_date.year)
        return returned_date

    # Apply correction directly to the rows identified by mask_future
    df.loc[mask_future, returned_col] = df.loc[mask_future].apply(
        lambda row: correct_year(row), axis=1
    )

    return df

def add_borrow_duration_and_alert(
    df: pd.DataFrame,
    checkout_col: str = 'Book checkout',
    returned_col: str = 'Book Returned',
    max_allowed_days: int = 14
) -> pd.DataFrame:
    """
    Adds a column for number of days borrowed and an alert:
    'ON TIME', 'OVERDUE', or 'SCHEDULED' for future due dates.
    """
    today = pd.to_datetime(datetime.now().date())

    # Ensure datetime format
    df[checkout_col] = pd.to_datetime(df[checkout_col], errors='coerce')
    df[returned_col] = pd.to_datetime(df[returned_col], errors='coerce')

    def calculate_duration(row):
        if pd.notna(row[returned_col]) and pd.notna(row[checkout_col]):
            return (row[returned_col] - row[checkout_col]).days
        elif pd.isna(row[returned_col]) and pd.notna(row[checkout_col]):
            return (today - row[checkout_col]).days
        else:
            return None

    def alert_status(row):
        duration = row['BorrowDuration']
        returned = row[returned_col]

        if pd.isna(returned):
            if duration is not None and duration > max_allowed_days:
                return 'OVERDUE'
            else:
                return 'SCHEDULED'
        else:
            return 'OVERDUE' if duration > max_allowed_days else 'ON TIME'

    # Add duration and alert columns
    df['BorrowDuration'] = df.apply(calculate_duration, axis=1)
    df['OverdueAlert'] = df.apply(alert_status, axis=1)

    return df

# Function to clean data (combines dropna, drop duplicates, and correct dates if applicable)
def clean_data(file_path: str, date_columns: list = [], output_file: str = "") -> pd.DataFrame:
    # Step 1: Read in the raw data
    rawData = read_csv(file_path)

    # Step 1.1: Replace blank strings or "NaN" strings with real NaN
    cleanData = rawData.replace(r'^\s*$', pd.NA, regex=True)
    cleanedData = cleanData.replace("NaN", pd.NA)

    # Step 2: Drop rows with all NaN values
    df_noNA = drop_na(cleanedData)

    # Optional: Drop rows missing critical fields (can customize per dataset)
    if 'Books' in df_noNA.columns and 'Customer ID' in df_noNA.columns:
        df_noNA = df_noNA[~(df_noNA["Books"].isna() & df_noNA["Customer ID"].isna())]

    # Step 3: Drop duplicate rows
    df_no_duplicates = drop_duplicates(df_noNA)

    # Step 4: Correct date columns if provided
    for date_column in date_columns:
        if date_column in df_no_duplicates.columns:
            df_no_duplicates = correct_dates(df_no_duplicates, date_column)

    # Step 5: Correct Checkout and Return dates
    if 'Book checkout' in df_no_duplicates.columns and 'Book Returned' in df_no_duplicates.columns:
        df_no_duplicates = fix_swapped_dates(df_no_duplicates)

    # Step 6: Correct incorrect dates in the data
    if 'Book checkout' in df_no_duplicates.columns and 'Book Returned' in df_no_duplicates.columns:
        df_no_duplicates = fix_swapped_and_future_dates(df_no_duplicates)

    # Step 7: Count the days customer holds the book and give an alert if it's longer than 14 days 
    if 'Book checkout' in df_no_duplicates.columns and 'Book Returned' in df_no_duplicates.columns:
        df_no_duplicates = add_borrow_duration_and_alert(df_no_duplicates)
    
    # Step 8: Save the cleaned data if output file path is provided
    if output_file:
        save_to_csv(df_no_duplicates, output_file)

    return df_no_duplicates