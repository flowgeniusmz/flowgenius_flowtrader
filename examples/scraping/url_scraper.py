import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import random
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from datetime import datetime, timedelta

# Define user agents to rotate through to avoid getting blocked
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]

# Parameters 
tickers = ['HOLO', 'DELL', 'SOUN', 'BABA', 'SMCI', 'MSFT', 'CVX', 'AMZN', 'ETN', 'AVGO', 'AMD']

# Base URL for scraping FinViz
finwiz_url = 'https://finviz.com/quote.ashx?t='
news_tables = {}

# Scraping News Data
for ticker in tickers:
    url = finwiz_url + ticker
    user_agent = random.choice(user_agents)
    req = Request(url=url, headers={'user-agent': user_agent})
    try:
        resp = urlopen(req)
        html = BeautifulSoup(resp, features="lxml")
        news_table = html.find(id='news-table')
        news_tables[ticker] = news_table
    except HTTPError as e:
        print(f"HTTPError for {ticker}: {e}")
    time.sleep(random.uniform(1, 3))  # Add delay to avoid getting blocked

# Print Recent News Headlines
try:
    for ticker in tickers:
        df = news_tables[ticker]
        if df is None:
            print(f"No news for {ticker}")
            continue
        df_tr = df.findAll('tr')

        print('\n')
        print(f'Headers for {ticker}: ')

        n = len(df_tr)  # Define n as the number of rows found
        for i, table_row in enumerate(df_tr):
            if table_row.a is None:
                continue  # Skip rows without an <a> tag

            a_text = table_row.a.text
            td_text = table_row.td.text.strip()
            print(a_text, '(', td_text, ')')
            if i == min(n-1, 5):  # Print up to 5 headlines, or all if fewer
                break
except KeyError:
    pass

# Parsing news data
parsed_news = []
for file_name, news_table in news_tables.items():
    if news_table is None:
        continue
    for x in news_table.findAll('tr'):
        if x.a is None:
            continue  # Skip rows without <a> tag
        text = x.a.get_text()
        date_scrape = x.td.text.split()

        if len(date_scrape) == 1:
            time = date_scrape[0]
            date = "Today"  # Assuming single time means today's news
        else:
            date = date_scrape[0]
            time = date_scrape[1]

        ticker = file_name
        parsed_news.append([ticker, date, time, text])

# Download the VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Sentiment Analysis
analyzer = SentimentIntensityAnalyzer()

# Convert parsed news data into a DataFrame
columns = ['Ticker', 'Date', 'Time', 'Headline']
news = pd.DataFrame(parsed_news, columns=columns)

# Define function to parse date with error handling
def parse_date(date_str):
    try:
        if date_str == "Today":
            return datetime.now().date()
        else:
            return datetime.strptime(date_str, '%b-%d').replace(year=datetime.now().year)
    except ValueError as e:
        print(f"Skipping invalid date format: {date_str}. Error: {e}")
        return None  # Return None for invalid dates

# Convert 'Date' column to actual dates
news['Date'] = news['Date'].apply(parse_date)

# Drop rows where the date couldn't be parsed
news = news.dropna(subset=['Date'])

# Perform sentiment analysis on the headlines
scores = news['Headline'].apply(analyzer.polarity_scores).tolist()
df_scores = pd.DataFrame(scores)
news = news.join(df_scores, rsuffix='_right')

# Group news by ticker
unique_ticker = news['Ticker'].unique().tolist()
news_dict = {name: news.loc[news['Ticker'] == name] for name in unique_ticker}

# Calculate average sentiment score for each ticker
values = []
for ticker in tickers:
    dataframe = news_dict.get(ticker)
    if dataframe is None or dataframe.empty:
        print(f"No news data for {ticker}")
        continue
    dataframe = dataframe.set_index('Ticker')
    dataframe = dataframe.drop(columns=['Headline'])
    print('\n')
    print(dataframe.head())

    mean = round(dataframe['compound'].mean(), 2)
    values.append(mean)

# Create a DataFrame of tickers and their average sentiment scores
df = pd.DataFrame(list(zip(tickers, values)), columns=['Ticker', 'Avg Sentiment'])
df = df.set_index('Ticker')
df = df.sort_values('Avg Sentiment', ascending=False)
print('\n')
print(df)
