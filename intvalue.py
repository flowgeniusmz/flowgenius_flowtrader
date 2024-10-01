# #https://medium.com/@bugragultekin/intrinsic-valuation-sentiment-analysis-driven-stock-screener-1660e921af69
# import requests
# from bs4 import BeautifulSoup
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from nltk import download
# import streamlit as st
# import pandas as pd
# import yfinance as yf
# import numpy as np

# # Constants for Intrinsic Value Calculation
# discount_rate = 0.10  # Discount rate (10%)
# growth_rate = 0.05    # Growth rate (5%)
# terminal_growth_rate = 0.03  # Terminal growth rate (3%)

# # Function to calculate the intrinsic value using the DCF model
# def calculate_intrinsic_value(eps, growth_rate, discount_rate, terminal_growth_rate, years=5):
#     intrinsic_value = 0
#     for year in range(1, years + 1):
#         intrinsic_value += eps * (1 + growth_rate) ** year / (1 + discount_rate) ** year
#     # Calculate terminal value
#     terminal_value = eps * (1 + growth_rate) ** years * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
#     terminal_value /= (1 + discount_rate) ** years
#     intrinsic_value += terminal_value
#     return intrinsic_value


# # Download VADER lexicon for sentiment analysis
# download('vader_lexicon')

# # Function to perform sentiment analysis using Finviz news headlines
# def analyze_sentiment_finviz(ticker):
#     finviz_url = f"https://finviz.com/quote.ashx?t={ticker}"
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

#     try:
#         response = requests.get(finviz_url, headers=headers)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Find the news items
#         news_table = soup.find('table', class_='news-table')
#         if not news_table:
#             st.warning(f"News table not found for {ticker} on Finviz.")
#             return [], 0

#         news_items = news_table.find_all('tr')
#         if not news_items:
#             st.warning(f"No news items found for {ticker} on Finviz.")
#             return [], 0

#         headlines = []
#         for item in news_items:
#             news_data = item.find_all('td')
#             if len(news_data) > 1:
#                 headline = news_data[1].get_text(strip=True)
#                 headlines.append(headline)

#         if not headlines:
#             st.warning(f"No headlines found for {ticker} on Finviz.")
#             return [], 0

#         # Filter out irrelevant headlines
#         relevant_headlines = [headline for headline in headlines if not any(keyword in headline.upper() for keyword in irrelevant_keywords)]

#         if not relevant_headlines:
#             st.warning(f"No relevant headlines found for {ticker} after filtering.")
#             return [], 0

#         analyzer = SentimentIntensityAnalyzer()
#         sentiments = [analyzer.polarity_scores(headline)['compound'] for headline in relevant_headlines]
#         average_sentiment = np.mean(sentiments) if sentiments else 0
#         return relevant_headlines, average_sentiment
#     except Exception as e:
#         st.error(f"Error retrieving news from Finviz for {ticker}: {e}")
#         return [], 0
    


# # Streamlit interface
# st.title("Intrinsic Valuation & Sentiment Analysis driven Stock Screener")

# # Layout setup with two columns: left for the table, right for the graphs
# col1, col2 = st.columns([1, 1.5])

# with col1:
#     st.subheader("Filtered Stocks")
#     max_stocks = st.slider("Select the maximum number of stocks to process", 10, 600, 100)
    
#     if 'filtered_stocks' not in st.session_state:
#         if st.button("Run Analysis"):
#             sp600_tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_600_companies')[0]['Symbol'].tolist()
#             filtered_stocks = []
#             progress = st.progress(0)

#             for i, ticker in enumerate(sp600_tickers[:max_stocks]):
#                 progress.progress(i / max_stocks)
#                 try:
#                     fixed_ticker = fix_ticker(ticker)
#                     stock = yf.Ticker(fixed_ticker)

#                     try:
#                         history = stock.history(period="1d")
#                         if history.empty:
#                             st.warning(f"No recent trading data available for {ticker}. Skipping...")
#                             continue
#                     except Exception as e:
#                         st.warning(f"Error retrieving history data for {ticker}: {e}")
#                         continue

#                     current_price = history['Close'].iloc[-1]
#                     eps = stock.info.get('trailingEps', None)
#                     pe_ratio = stock.info.get('trailingPE', None)

#                     if eps and eps > 0:
#                         intrinsic_value = calculate_intrinsic_value(eps, growth_rate, discount_rate, terminal_growth_rate)

#                         if intrinsic_value > current_price and pe_ratio > 10 and pe_ratio < 20:
#                             sentiment_score_finviz = analyze_sentiment_finviz(ticker)[1]

#                             if sentiment_score_finviz > 0:
#                                 filtered_stocks.append({
#                                     'Ticker': ticker,
#                                     'Current Price': current_price,
#                                     'Intrinsic Value': intrinsic_value,
#                                     'P/E Ratio': pe_ratio,
#                                     'EPS': eps,
#                                     'Sentiment Score (Finviz)': sentiment_score_finviz
#                                 })
                
#                 except IndexError:
#                     st.warning(f"Could not retrieve data for {ticker}, possibly due to no recent trading data.")
#                 except Exception as e:
#                     st.warning(f"Could not process {ticker}: {e}")

#             if filtered_stocks:
#                 st.session_state.filtered_stocks = pd.DataFrame(filtered_stocks)
#             else:
#                 st.session_state.filtered_stocks = pd.DataFrame()

#             progress.empty()

#     # Check if filtered_stocks is populated and contains the 'Ticker' column
#     if 'filtered_stocks' in st.session_state and not st.session_state.filtered_stocks.empty:
#         if 'Ticker' in st.session_state.filtered_stocks.columns:
#             selected_ticker = st.selectbox("Select a ticker to view details", st.session_state.filtered_stocks['Ticker'])
#             st.dataframe(st.session_state.filtered_stocks)

#             # Display company info and latest news
#             if selected_ticker:
#                 sector, industry, description, latest_news, dividend_rate = get_company_info(selected_ticker)
#                 st.subheader(f"Company Information: {selected_ticker}")
#                 st.write(f"**Sector:** {sector}")
#                 st.write(f"**Industry:** {industry}")
#                 st.write(f"**Brief Description:** {description}")
#                 st.write(f"**Dividend Rate:** {dividend_rate}")
#                 st.write("**Latest News:**")
                
#                 for news in latest_news:
#                     st.write(f"- {news}")
#         else:
#             st.error("The filtered stocks DataFrame does not contain a 'Ticker' column.")
#     else:
#         st.warning("No stocks have been filtered yet.")

# with col2:
#     if 'filtered_stocks' in st.session_state and 'Ticker' in st.session_state.filtered_stocks.columns and not st.session_state.filtered_stocks.empty:
#         st.subheader(f"Trend Analysis for {selected_ticker}")

#         # Add a select box to choose the time period
#         time_period = st.radio("Select time period", ["1mo", "3mo", "6mo"], index=2, horizontal=True)

#         # Define time periods
#         time_period_map = {
#             "1mo": "1mo",
#             "3mo": "3mo",
#             "6mo": "6mo"
#         }
#         period = time_period_map.get(time_period, "6mo")

#         # Retrieve stock data for the selected period
#         stock = yf.Ticker(fix_ticker(selected_ticker))
#         history = stock.history(period=period)

#         # Calculate RSI and MACD
#         history['RSI'] = calculate_rsi(history)
#         history['MACD'], history['Signal Line'] = calculate_macd(history)

#         # Create subplots: Candlestick with MACD on a separate axis
#         fig = go.Figure()

#         # Candlestick chart
#         fig.add_trace(go.Candlestick(x=history.index,
#                                      open=history['Open'],
#                                      high=history['High'],
#                                      low=history['Low'],
#                                      close=history['Close'],
#                                      name='Candlestick'))

#         # MACD
#         fig.add_trace(go.Scatter(x=history.index, y=history['MACD'], line=dict(color='green', width=1), name='MACD', yaxis='y2'))
#         fig.add_trace(go.Scatter(x=history.index, y=history['Signal Line'], line=dict(color='red', width=1), name='Signal Line', yaxis='y2'))

#         # Update layout to include secondary y-axis for MACD
#         fig.update_layout(
#             title=f"Candlestick Chart with MACD - {time_period}",
#             xaxis_title="Date",
#             yaxis_title="Price",
#             yaxis2=dict(title="MACD", overlaying='y', side='right'),
#             height=500
#         )

#         # Display the charts
#         st.plotly_chart(fig)

#         # Display RSI
#         st.write("RSI (Relative Strength Index) is a momentum oscillator that measures the speed and change of price movements. RSI values above 70 are considered overbought, and below 30 are considered oversold.")
#         st.line_chart(history['RSI'])