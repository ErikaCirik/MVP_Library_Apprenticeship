import argparse
import pandas as pd
from utils.booksAPIFetch import enrich_books
import utils.projectFunctions as projectFunctions

# Set up command-line arguments
parser = argparse.ArgumentParser(description="Clean library data and optionally write to SQL Server.")
parser.add_argument("--write-to-sql", action="store_true", help="Write cleaned data to SQL Server")
args = parser.parse_args()

# --- Clean Customer Data ---
customer_cleaned = projectFunctions.clean_data(
    "./raw_data/03_Library SystemCustomers.csv",
    output_file="./output/customerCleanedPy.csv"
)
print("✅ Customer data cleansed.")

# --- Clean Book Data (with date correction) ---
book_cleaned = projectFunctions.clean_data(
    "./raw_data/03_Library Systembook.csv",
    date_columns=['Book checkout', 'Book Returned'],
    output_file="./output/bookCleanedPy.csv"
)
print("✅ Book data cleansed.")

# --- Clean Books Enhanced API Information ---
# Enrich with Open Library API
df_enriched = enrich_books(book_cleaned)
df_enriched.to_csv("./raw_data/bookEnrichedWithAPI.csv", index=False)
print("✅ Book data enriched.")

book_api = projectFunctions.clean_data(
    "./raw_data/bookEnrichedWithAPI.csv",
    output_file="./output/bookEnrichedAPICleanedPy.csv"
)
print("✅ Book Enriched data cleansed.")

# --- Load Cleaned CSVs ---
df_customer = pd.read_csv('./output/customerCleanedPy.csv')
df_book = pd.read_csv('./output/bookCleanedPy.csv')
df_bookEnriched = pd.read_csv('./output/bookEnrichedAPICleanedPy.csv')
print("✅ All cleansed CSVs loaded.")

# --- Optional SQL Write ---
if args.write_to_sql:
    from utils.loadToServer import write_df_to_sql
    write_df_to_sql(df_book, table_name='Books', database='MVP_Library')
    write_df_to_sql(df_customer, table_name='Customers', database='MVP_Library')
    write_df_to_sql(df_bookEnriched, table_name='BooksEnriched', database='MVP_Library')
    print("✅ Data written to SQL Server.")
else:
    print("⚠️ SQL write skipped. Use --write-to-sql to enable.")
