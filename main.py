import streamlit as st
import pandas as pd
import numpy as np
from clsAlpaca import AlpacaStock
import ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    

     # Add moving averages
    df['ma_short'] = df['close'].rolling(window=5).mean()
    df['ma_long'] = df['close'].rolling(window=20).mean()
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
        ma_crossover_buy = (df['ma_short'].iloc[i] > df['ma_long'].iloc[i] and df['ma_short'].iloc[i-1] <= df['ma_long'].iloc[i-1])
        ma_crossover_sell = (df['ma_short'].iloc[i] < df['ma_long'].iloc[i] and df['ma_short'].iloc[i-1] >= df['ma_long'].iloc[i-1])
        # Buy Signal
        buy_conditions = [ma_crossover_buy, macd_cross_up, rsi_oversold, price_near_lower_band]
        if sum(buy_conditions) >= 3:
            df.at[df.index[i], 'signal'] = 1  # Buy signal

        # Sell Signal
        sell_conditions = [ma_crossover_sell, macd_cross_down, rsi_overbought, price_near_upper_band]
        if sum(sell_conditions) >= 3:
            df.at[df.index[i], 'signal'] = -1  # Sell signal

    return df

# def plot_chart_with_signals(df):
#     # Create subplots
#     fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
#                         vertical_spacing=0.02, subplot_titles=('OHLC', 'MACD', 'RSI'),
#                         row_width=[0.2, 0.2, 0.6])

#     # Add OHLC chart
#     fig.add_trace(go.Candlestick(x=df['timestamp'],
#                                  open=df['open'],
#                                  high=df['high'],
#                                  low=df['low'],
#                                  close=df['close'],
#                                  name='OHLC'), row=1, col=1)

#     # Add buy/sell signals on OHLC chart
#     buy_signals = df[df['signal'] == 1]
#     sell_signals = df[df['signal'] == -1]
#     fig.add_trace(go.Scatter(x=buy_signals['timestamp'],
#                              y=buy_signals['close'],
#                              mode='markers',
#                              marker_symbol='triangle-up',
#                              marker_color='green',
#                              marker_size=10,
#                              name='Buy Signal'), row=1, col=1)
#     fig.add_trace(go.Scatter(x=sell_signals['timestamp'],
#                              y=sell_signals['close'],
#                              mode='markers',
#                              marker_symbol='triangle-down',
#                              marker_color='red',
#                              marker_size=10,
#                              name='Sell Signal'), row=1, col=1)

#     # Add MACD
#     fig.add_trace(go.Scatter(x=df['timestamp'], y=df['macd'], name='MACD'), row=2, col=1)
#     fig.add_trace(go.Scatter(x=df['timestamp'], y=df['macd_signal'], name='Signal Line'), row=2, col=1)

#     # Add RSI
#     fig.add_trace(go.Scatter(x=df['timestamp'], y=df['rsi'], name='RSI'), row=3, col=1)
#     fig.add_hline(y=70, line_dash='dash', row=3, col=1)
#     fig.add_hline(y=30, line_dash='dash', row=3, col=1)

#     # Update layout
#     fig.update_layout(title='Stock Price with Buy/Sell Signals and Indicators',
#                       xaxis_title='Time',
#                       yaxis_title='Price',
#                       height=900)

#     st.plotly_chart(fig)

def plot_chart_with_signals(df):
    from plotly.subplots import make_subplots

    # Create subplots with shared x-axis
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        vertical_spacing=0.02,
                        subplot_titles=('OHLC with Buy/Sell Signals and Moving Averages', 'MACD', 'RSI'))

    # Add candlestick chart in the first subplot
    fig.add_trace(go.Candlestick(
        x=df['timestamp'],
        open=df['open'],
        high=df['high'],
        low=df['low'],
        close=df['close'],
        name='OHLC'
    ), row=1, col=1)

    # Add moving averages to the first subplot
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['ma_short'],
        line=dict(color='blue', width=1),
        name='MA Short'
    ), row=1, col=1)
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['ma_long'],
        line=dict(color='orange', width=1),
        name='MA Long'
    ), row=1, col=1)

    # Add buy signals to the first subplot
    buy_signals = df[df['signal'] == 1]
    fig.add_trace(go.Scatter(
        x=buy_signals['timestamp'],
        y=buy_signals['close'],
        mode='markers',
        marker_symbol='triangle-up',
        marker_color='green',
        marker_size=12,
        name='Buy Signal'
    ), row=1, col=1)

    # Add sell signals to the first subplot
    sell_signals = df[df['signal'] == -1]
    fig.add_trace(go.Scatter(
        x=sell_signals['timestamp'],
        y=sell_signals['close'],
        mode='markers',
        marker_symbol='triangle-down',
        marker_color='red',
        marker_size=12,
        name='Sell Signal'
    ), row=1, col=1)

    # Add MACD to the second subplot
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['macd'],
        line=dict(color='blue', width=1),
        name='MACD Line'
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['macd_signal'],
        line=dict(color='red', width=1),
        name='Signal Line'
    ), row=2, col=1)
    fig.add_trace(go.Bar(
        x=df['timestamp'],
        y=df['macd'] - df['macd_signal'],
        name='MACD Histogram'
    ), row=2, col=1)

    # Add RSI to the third subplot
    fig.add_trace(go.Scatter(
        x=df['timestamp'],
        y=df['rsi'],
        line=dict(color='purple', width=1),
        name='RSI'
    ), row=3, col=1)
    # Add overbought/oversold lines
    fig.add_hline(y=70, line_dash='dash', line_color='red', row=3, col=1)
    fig.add_hline(y=30, line_dash='dash', line_color='green', row=3, col=1)

    # Update layout
    fig.update_layout(
        title='Stock Price with Buy/Sell Signals and Indicators',
        xaxis_title='Time',
        height=900, 
        legend=dict(orientation="v", yanchor="bottom", y=1, xanchor="right", x=1)
    )

    st.plotly_chart(fig)

    
# Initialize session state variables for historical and streaming data
if "historical_stock_data" not in st.session_state:
    st.session_state.historical_stock_data = get_historical_data(ticker="DJT")
    st.session_state.historical_stock_data = compute_indicators(st.session_state.historical_stock_data)
    st.session_state.historical_stock_data = generate_signals(st.session_state.historical_stock_data)

if "streaming_stock_data" not in st.session_state:
    st.session_state.streaming_stock_data = st.session_state.historical_stock_data.copy()

# FraDJTnt function to continuously update streaming data every 1 second
@st.fragment(run_every="30s")
def update_streaming_data():
    latest_data = get_latest_data(ticker="DJT")

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
st.write("RSI Min:", st.session_state.streaming_stock_data['rsi'].min())
st.write("RSI Max:", st.session_state.streaming_stock_data['rsi'].max())
st.write("MACD Min:", st.session_state.streaming_stock_data['macd'].min())
st.write("MACD Max:", st.session_state.streaming_stock_data['macd'].max())

# Run the fraDJTnt to start streaming updates
update_streaming_data()
