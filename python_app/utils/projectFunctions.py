import pandas as pd

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
    df[column_name] = df[column_name].str.replace('"', '', regex=False)
    df[column_name] = df[column_name].apply(
        lambda x: x if len(x.split('/')) == 3 and int(x.split('/')[0]) <= 31 else default_date
    )
    df[column_name] = pd.to_datetime(df[column_name], dayfirst=True)
    return df

# Function to save a cleaned dataframe to a CSV file
def save_to_csv(df: pd.DataFrame, output_file: str) -> None:
    df.to_csv(output_file, index=False)

# Function to clean data (combines dropna, drop duplicates, and correct dates if applicable)
def clean_data(file_path: str, date_columns: list = [], output_file: str = "") -> pd.DataFrame:
    # Step 1: Read in the raw data
    df = read_csv(file_path)
    
    # Step 2: Drop rows with all NaN values
    df_cleaned = drop_na(df)
    
    # Step 3: Drop duplicate rows
    df_no_duplicates = drop_duplicates(df_cleaned)
    
    # Step 4: Correct date columns if provided
    for date_column in date_columns:
        df_no_duplicates = correct_dates(df_no_duplicates, date_column)
    
    # Step 5: Save the cleaned data if output file path is provided
    if output_file:
        save_to_csv(df_no_duplicates, output_file)
    
    return df_no_duplicates