import utils.projectFunctions as projectFunctions

# Usage example for customer data
customer_cleaned = projectFunctions.clean_data("C:/Users/Admin/MVP_Library_Apprenticeship/python_app/raw_data/03_Library SystemCustomers.csv", output_file="output/customerCleanedPy.csv")

# Usage example for book data with date correction
book_cleaned = projectFunctions.clean_data("C:/Users/Admin/MVP_Library_Apprenticeship/python_app/raw_data/03_Library Systembook.csv", 
                          date_columns=['Book checkout', 'Book Returned'], output_file="output/bookCleanedPy.csv")
