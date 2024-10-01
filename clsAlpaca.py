import streamlit as st
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import StockBarsRequest, StockLatestBarRequest, NewsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from datetime import datetime, timedelta, timezone
import nest_asyncio
nest_asyncio.apply()


class AlpacaStock:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.initialize()        

    def initialize(self):
        self._initialize_variables()
        self._initialize_clients()
        self._initialize_requests()
    
    def _initialize_variables(self):
        self.symbol = None
        self.open = None
        self.high = None
        self.close = None
        self.low = None
        self.volume = None
        self.vwap = None
        self.timestamp = None
        self.trade_count = None
        self.current_datetime = datetime.now(timezone.utc)
        self.lookback_datetime = self.current_datetime - timedelta(hours=160)
        self.lookback_datetime_stripped = self.lookback_datetime.date().strftime("%Y-%m-%d")
    
    def _initialize_clients(self):
        self.stockdataclient = StockHistoricalDataClient(api_key=st.secrets.alpaca.api_key_paper, secret_key=st.secrets.alpaca.secret_key_paper)
        self.newsclient = NewsClient(api_key=st.secrets.alpaca.api_key_paper, secret_key=st.secrets.alpaca.secret_key_paper)

    def _initialize_requests(self):
        self.request_params_stocklatestbar = StockLatestBarRequest(symbol_or_symbols=self.ticker)
        self.request_params_stockhistorical = StockBarsRequest(symbol_or_symbols=[self.ticker], timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute))
        self.request_params_news = NewsRequest(symbols=self.ticker, start=self.lookback_datetime)

    
    def get_historical_bars(self):
        self.historical_bars = self.stockdataclient.get_stock_bars(request_params=self.request_params_stockhistorical)
        self.historical_data = self.historical_bars[self.ticker]
        # Convert to DataFrame
        self.historical_df = self.historical_bars.df
        return self.historical_df

    def get_latest_bars(self):
        self.latest_bars = self.stockdataclient.get_stock_latest_bar(request_params=self.request_params_stocklatestbar)
        self.latest_bar_data = self.latest_bars[self.ticker]
        self.latest_bar_data_dict = self.latest_bar_data.model_dump()
        self.latest_bar_df = pd.DataFrame([self.latest_bar_data_dict])
        print(self.latest_bar_df)
        return self.latest_bar_df

    def get_news(self):
        self.news = self.newsclient.get_news(request_params=self.request_params_news)
        self.news_df = self.news.df
        return self.news_df


# a = AlpacaStock(ticker="GME")
# latest = a.get_latest_bars()
# news = a.get_news()





