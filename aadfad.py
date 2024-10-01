import streamlit as st
import pandas as pd
import mplfinance as mpf
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest, StockLatestBarRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import nest_asyncio
nest_asyncio.apply()

# ------------------------------
# Streamlit Page Configuration
# ------------------------------
st.set_page_config(page_title="FlowTrader", page_icon="assets/images/flowtrader_icon1.png", layout="wide", initial_sidebar_state="collapsed")

# ------------------------------
# # Set Functions
# # ------------------------------
# def get_historical_bars(ticker: str):
#     client = StockHistoricalDataClient(api_key=st.secrets.alpaca.api_key, secret_key=st.secrets.alpaca.secret_key)
#     request_params = StockBarsRequest(symbol_or_symbols=[ticker], timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute))
#     bars = client.get_stock_bars(request_params)

#     # Manually extract data from the response and create a DataFrame
#     data = []
#     for bar in bars[ticker]:
#         new_row = {
#             'timestamp': bar.timestamp,
#             'open': bar.open,
#             'high': bar.high,
#             'low': bar.low,
#             'close': bar.close,
#             'volume': bar.volume,
#             'trade_count': bar.trade_count
#         }
#         data.append(new_row)
#     bars_df = pd.DataFrame(data)

#     # Ensure timestamp is in datetime format and set as index
#     bars_df['timestamp'] = pd.to_datetime(bars_df['timestamp'], errors='coerce')
#     bars_df.dropna(subset=['timestamp'], inplace=True)
#     bars_df.set_index('timestamp', inplace=True)

#     return bars_df

# a = get_historical_bars(ticker="GME")
# a.to_csv("data.csv")
# print(a)


def get_latest_bars(ticker: str):
    client = StockHistoricalDataClient(api_key=st.secrets.alpaca.api_key, secret_key=st.secrets.alpaca.secret_key)
    request_params = StockLatestBarRequest(symbol_or_symbols=ticker)
    bar = client.get_stock_latest_bar(request_params=request_params)
    bar_ticker = bar[ticker]
    bar_data = bar_ticker.dict()
    bar_df = pd.DataFrame([bar_data])
    print(bar)
    print(bar_ticker)
    print(bar_data)
    print(bar_df)
print(get_latest_bars(ticker="GME"))

 