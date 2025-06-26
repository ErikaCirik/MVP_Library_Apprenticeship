import streamlit as st
import pandas as pd
import sys
import os

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

#to run: python -m streamlit run streamlitDashboard.py