import streamlit as st
import pandas as pd
from clsAlpaca import AlpacaStock
import plotly.graph_objects as go

# Function to fetch historical data
@st.cache_data(ttl=10)
def get_historical_data(ticker: str):
    stock_class = AlpacaStock(ticker=ticker)
    stock_historical_df = stock_class.get_historical_bars()
    # Reset index to make timestamp and symbol regular columns
    stock_historical_df.reset_index(inplace=True)
    print(stock_historical_df)
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

# Fragment function to continuously update streaming data every 1 second
@st.fragment(run_every="60s")
def update_streaming_data():
    latest_data = get_latest_data(ticker="GME")
    
    # Append latest data to the streaming DataFrame in session state
    st.session_state.streaming_stock_data = pd.concat(
        [st.session_state.streaming_stock_data, latest_data],
        ignore_index=True
    )
    st.toast("updated")
    
    # Display the updated DataFrame
    st.dataframe(st.session_state.streaming_stock_data)

    # Display a bar chart of the stock's OHLC (Open, High, Low, Close) data
    if not st.session_state.streaming_stock_data.empty:
        ohlc_chart_data = st.session_state.streaming_stock_data[['timestamp', 'open', 'high', 'low', 'close']]
        ohlc_chart_data = ohlc_chart_data.set_index('timestamp')

        # Plot the stock bars using Streamlit's line chart for simplicity (consider candlestick charts for more complex visualizations)
        st.line_chart(ohlc_chart_data[['open', 'high', 'low', 'close']])

        # Create a candlestick chart using Plotly
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc_chart_data.index,
            open=ohlc_chart_data['open'],
            high=ohlc_chart_data['high'],
            low=ohlc_chart_data['low'],
            close=ohlc_chart_data['close']
        )])

        # Render the Plotly chart in Streamlit
        st.plotly_chart(fig)

# Set the title of the app
st.title("Live Streaming Stock Data")

main_container = st.container()
with main_container:
    cols = st.columns([1,20,1])
    with cols[1]:
        # Run the fragment to start streaming updates
        update_streaming_data()
