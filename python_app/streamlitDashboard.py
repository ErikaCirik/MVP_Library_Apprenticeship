import streamlit as st
import pandas as pd
from utils.DE_metrics import get_num_customers, get_num_books, get_num_api_requests

customers = pd.read_csv("output/customerCleanedPy.csv")
books = pd.read_csv("output/bookCleanedPy.csv")
api_books = pd.read_csv("output/bookEnrichedAPICleanedPy.csv")

st.metric("Number of Customers", get_num_customers(customers))
st.metric("Number of Books", get_num_books(books))
st.metric("Number of API Requests", get_num_api_requests(api_books))