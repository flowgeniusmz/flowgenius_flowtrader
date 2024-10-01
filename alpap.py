# import streamlit as st
# import pandas as pd
# import mplfinance as mpf
# import time
# from alpaca.data.historical import StockHistoricalDataClient
# from alpaca.data.requests import StockBarsRequest, StockLatestBarRequest
# from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
# import nest_asyncio
# nest_asyncio.apply()

# st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# def get_historical_bars(ticker: str):
#     client = StockHistoricalDataClient(api_key = st.secrets.alpaca.api_key, secret_key=st.secrets.alpaca.secret_key)
#     request_params = StockBarsRequest(symbol_or_symbols = [ticker], timeframe = TimeFrame(amount = 1, unit = TimeFrameUnit.Minute))
#     bars = client.get_stock_bars(request_params)
#     print(bars)
#     bars_df = bars.df
#     return bars_df  

# def get_latest_bars(ticker: str):
#     client = StockHistoricalDataClient(api_key=st.secrets.alpaca.api_key, secret_key=st.secrets.alpaca.secret_key)
#     request_params = StockLatestBarRequest(symbol_or_symbols = ticker)
#     bar = client.get_stock_latest_bar(request_params=request_params)
    
#     # Extract relevant data from the bar object
#     bar_data = {
#         'open': bar[ticker].open,
#         'high': bar[ticker].high,
#         'low': bar[ticker].low,
#         'close': bar[ticker].close,
#         'volume': bar[ticker].volume,
#         'timestamp': bar[ticker].timestamp,
#         'trade_count': bar[ticker].trade_count
#     }
    
#     # Convert the extracted data into a DataFrame
#     bar_df = pd.DataFrame([bar_data])
    
#     # Concatenate the latest bar with the existing dataframe
#     st.session_state.df_bars = pd.concat([st.session_state.df_bars, bar_df], ignore_index=True)

# @st.fragment(run_every="20s")
# def updated_dataframe():
#     get_latest_bars(ticker=ticker)
#     st.toast("Updated")
#     display_container = st.container()
#     other_container = st.container()
#     with display_container:
#         df = st.dataframe(st.session_state.df_bars, use_container_width=True)
#     # with other_container:
#     #     fig, ax = mpf.plot(
#     #     st.session_state.df_bars,
#     #     type='candle', 
#     #     style='charles',
#     #     title='Candlestick Chart',
#     #     ylabel='Price',
#     #     volume=True,
#     #     returnfig=True
#     # )

# # ticker = "GME"

# # if "df_bars" not in st.session_state:
# #     st.session_state.df_bars = get_historical_bars(ticker=ticker)

# # st.title("GME")
# # updated_dataframe()

# print(get_historical_bars(ticker="GME"))
