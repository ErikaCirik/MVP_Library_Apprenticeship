import streamlit as st
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

# Add the parent directory of the project to sys.path so 'utils' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

try:
    from utils.DE_metrics import get_num_customers, get_num_books, get_num_api_requests
except ModuleNotFoundError:
    # Try absolute path if running from a different working directory
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
    from DE_metrics import get_num_customers, get_num_books, get_num_api_requests

customers = pd.read_csv("output/customerCleanedPy.csv")
books = pd.read_csv("output/bookCleanedPy.csv")
api_books = pd.read_csv("output/bookEnrichedAPICleanedPy.csv")

st.metric("Number of Customers", get_num_customers(customers))
st.metric("Number of Books", get_num_books(books))
st.metric("Number of API Requests", get_num_api_requests(api_books))

# Example: Bar chart of top 5 most borrowed books
st.subheader("Top 5 Most Borrowed Books")
top_books = books["Books"].value_counts().head(5)
st.bar_chart(top_books.rename_axis("Book Title").rename("Number of Borrows"))

# Example: Pie chart of overdue vs on time
if "OverdueAlert" in books.columns:
    st.write("Overdue vs On Time Returns")
    st.pyplot(books["OverdueAlert"].value_counts().plot.pie(autopct='%1.1f%%', figsize=(4,4)).get_figure())

# Example: Histogram of borrow durations
if "BorrowDuration" in books.columns:
    st.write("Borrow Duration Distribution")
    st.bar_chart(books["BorrowDuration"].dropna())

#to run: python -m streamlit run streamlitDashboard.py --server.port 8502