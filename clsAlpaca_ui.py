import streamlit as st
import pandas as pd
from clsAlpaca import AlpacaStock
import time

# Function to fetch historical data
@st.cache_data(ttl=10)
def get_historical_data(ticker: str):
    stock_class = AlpacaStock(ticker=ticker)
    stock_historical_df = stock_class.get_historical_bars()
    return stock_historical_df

# Function to fetch the latest data
def get_latest_data(ticker: str):
    stock_class = AlpacaStock(ticker=ticker)
    stock_latest_df = stock_class.get_latest_bars()
    return stock_latest_df

# Initialize session state variables for historical and streaming data
if "historical_stock_data" not in st.session_state:
    st.session_state.historical_stock_data = get_historical_data(ticker="GME")

if "streaming_stock_data" not in st.session_state:
    st.session_state.streaming_stock_data = st.session_state.historical_stock_data.copy()

# Function to continuously update streaming data
def update_streaming_data():
    latest_data = get_latest_data(ticker="GME")
    st.session_state.streaming_stock_data = pd.concat(
        [st.session_state.streaming_stock_data, latest_data],
        ignore_index=True
    )

# Display the streaming data and update it every second
st.title("Streaming Stock Data")
stock_data_placeholder = st.empty()  # Placeholder for the DataFrame display

while True:
    update_streaming_data()
    stock_data_placeholder.dataframe(st.session_state.streaming_stock_data)
    time.sleep(1)  # Update every 1 second
