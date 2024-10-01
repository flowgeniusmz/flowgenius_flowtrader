import streamlit as st
import pandas as pd
import numpy as np
from clsAlpaca import AlpacaStock
import ta
import plotly.graph_objects as go


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
# Function to fetch historical data
@st.cache_data(ttl=10)
def get_historical_data(ticker: str):
    stock_class = AlpacaStock(ticker=ticker)
    stock_historical_df = stock_class.get_historical_bars()

    # Reset index to make timestamp and symbol regular columns
    stock_historical_df.reset_index(inplace=True)

    return stock_historical_df

# Function to fetch the latest data
def get_latest_data(ticker: str):
    stock_class = AlpacaStock(ticker=ticker)
    stock_latest_df = stock_class.get_latest_bars()

    # Reset index to make timestamp and symbol regular columns if needed
    stock_latest_df.reset_index(inplace=True)

    return stock_latest_df

def compute_indicators(df):
    # Ensure the DataFrame is sorted by timestamp
    df.sort_values(by='timestamp', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Compute MACD
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()
    
    # Compute RSI
    rsi = ta.momentum.RSIIndicator(close=df['close'])
    df['rsi'] = rsi.rsi()
    
    # Compute Bollinger Bands
    bb = ta.volatility.BollingerBands(close=df['close'])
    df['bb_mavg'] = bb.bollinger_mavg()
    df['bb_hband'] = bb.bollinger_hband()
    df['bb_lband'] = bb.bollinger_lband()
    
    # Compute Ichimoku Cloud
    ichimoku = ta.trend.IchimokuIndicator(high=df['high'], low=df['low'])
    df['ichimoku_a'] = ichimoku.ichimoku_a()
    df['ichimoku_b'] = ichimoku.ichimoku_b()
    df['ichimoku_base_line'] = ichimoku.ichimoku_base_line()
    df['ichimoku_conversion_line'] = ichimoku.ichimoku_conversion_line()
    
    # Compute Keltner Channels
    kc = ta.volatility.KeltnerChannel(high=df['high'], low=df['low'], close=df['close'])
    df['kc_mband'] = kc.keltner_channel_mband()
    df['kc_hband'] = kc.keltner_channel_hband()
    df['kc_lband'] = kc.keltner_channel_lband()
    
    return df

def generate_signals(df):
    # Initialize signal column if it doesn't exist
    if 'signal' not in df.columns:
        df['signal'] = 0

    # Logic for generating buy/sell signals
    for i in range(1, len(df)):
        # Conditions
        macd_cross_up = df['macd'].iloc[i] > df['macd_signal'].iloc[i] and df['macd'].iloc[i-1] <= df['macd_signal'].iloc[i-1]
        macd_cross_down = df['macd'].iloc[i] < df['macd_signal'].iloc[i] and df['macd'].iloc[i-1] >= df['macd_signal'].iloc[i-1]
        rsi_oversold = df['rsi'].iloc[i] < 45  # Adjusted threshold
        rsi_overbought = df['rsi'].iloc[i] > 55  # Adjusted threshold
        price_near_lower_band = df['close'].iloc[i] < df['bb_lband'].iloc[i] * 1.01  # Within 1% of lower band
        price_near_upper_band = df['close'].iloc[i] > df['bb_hband'].iloc[i] * 0.99  # Within 1% of upper band

        # Buy Signal
        buy_conditions = [macd_cross_up, rsi_oversold, price_near_lower_band]
        if sum(buy_conditions) >= 2:
            df.at[df.index[i], 'signal'] = 1  # Buy signal

        # Sell Signal
        sell_conditions = [macd_cross_down, rsi_overbought, price_near_upper_band]
        if sum(sell_conditions) >= 2:
            df.at[df.index[i], 'signal'] = -1  # Sell signal

    return df

def plot_chart_with_signals(df):
    fig = go.Figure()
    
    # Add candlestick chart
    fig.add_trace(go.Candlestick(x=df['timestamp'],
                                 open=df['open'],
                                 high=df['high'],
                                 low=df['low'],
                                 close=df['close'],
                                 name='OHLC'))
    
    # Add buy signals
    buy_signals = df[df['signal'] == 1]
    fig.add_trace(go.Scatter(x=buy_signals['timestamp'],
                             y=buy_signals['close'],
                             mode='markers',
                             marker_symbol='triangle-up',
                             marker_color='green',
                             marker_size=10,
                             name='Buy Signal'))
    
    # Add sell signals
    sell_signals = df[df['signal'] == -1]
    fig.add_trace(go.Scatter(x=sell_signals['timestamp'],
                             y=sell_signals['close'],
                             mode='markers',
                             marker_symbol='triangle-down',
                             marker_color='red',
                             marker_size=10,
                             name='Sell Signal'))
    
    # Update layout
    fig.update_layout(title='Stock Price with Buy/Sell Signals',
                      xaxis_title='Time',
                      yaxis_title='Price')
    
    st.plotly_chart(fig)
    
# Initialize session state variables for historical and streaming data
if "historical_stock_data" not in st.session_state:
    st.session_state.historical_stock_data = get_historical_data(ticker="GME")
    st.session_state.historical_stock_data = compute_indicators(st.session_state.historical_stock_data)
    st.session_state.historical_stock_data = generate_signals(st.session_state.historical_stock_data)

if "streaming_stock_data" not in st.session_state:
    st.session_state.streaming_stock_data = st.session_state.historical_stock_data.copy()

# Fragment function to continuously update streaming data every 1 second
@st.fragment(run_every=1)
def update_streaming_data():
    latest_data = get_latest_data(ticker="GME")

    # Append latest data to the streaming DataFrame in session state
    st.session_state.streaming_stock_data = pd.concat(
        [st.session_state.streaming_stock_data, latest_data],
        ignore_index=True
    )

    # Remove duplicate timestamps (if any) to avoid conflicts
    st.session_state.streaming_stock_data.drop_duplicates(subset='timestamp', inplace=True)

    # Ensure data is sorted by timestamp
    st.session_state.streaming_stock_data.sort_values(by='timestamp', inplace=True)
    st.session_state.streaming_stock_data.reset_index(drop=True, inplace=True)

    # Recompute indicators and signals for the entire dataset
    st.session_state.streaming_stock_data = compute_indicators(st.session_state.streaming_stock_data)
    st.session_state.streaming_stock_data = generate_signals(st.session_state.streaming_stock_data)

    # Display the updated DataFrame with the most recent data at the top
    st.dataframe(st.session_state.streaming_stock_data.iloc[::-1])

    # Plot the stock chart with buy/sell signals
    if not st.session_state.streaming_stock_data.empty:
        plot_chart_with_signals(st.session_state.streaming_stock_data)

# Set the title of the app
st.title("Live Streaming Stock Data with Buy/Sell Signals")
st.write("Indicator Summary:")
st.write(st.session_state.historical_stock_data[['macd', 'macd_signal', 'rsi', 'bb_lband', 'bb_hband']].describe())

# Run the fragment to start streaming updates
update_streaming_data()
