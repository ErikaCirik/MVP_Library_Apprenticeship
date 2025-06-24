import pandas as pd
from utils.loadToServer import write_df_to_sql
import utils.projectFunctions as projectFunctions

# Usage example for customer data
customer_cleaned = projectFunctions.clean_data("C:/Users/Admin/MVP_Library_Apprenticeship/python_app/raw_data/03_Library SystemCustomers.csv", output_file="output/customerCleanedPy.csv")

# Usage example for book data with date correction
book_cleaned = projectFunctions.clean_data("C:/Users/Admin/MVP_Library_Apprenticeship/python_app/raw_data/03_Library Systembook.csv", 
                          date_columns=['Book checkout', 'Book Returned'], output_file="output/bookCleanedPy.csv")

# Load cleaned CSVs
df_customer = pd.read_csv('C:/Users/Admin/MVP_Library_Apprenticeship/Python_app/output/customerCleanedPy.csv')
df_book = pd.read_csv('C:/Users/Admin/MVP_Library_Apprenticeship/Python_app/output/bookCleanedPy.csv')

# Write to SQL
write_df_to_sql(df_book, table_name='Books', database='MVP_Library')
write_df_to_sql(df_customer, table_name='Customers', database='MVP_Library')