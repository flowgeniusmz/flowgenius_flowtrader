from newsapi import NewsApiClient
import streamlit as st
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

newsClient = NewsApiClient(api_key=st.secrets.newsapi.api_key)
top_headlines = newsClient.get_everything(q="GME", language="en") #, category="business", language="en", country="us")
articles = top_headlines['articles']
titles = []
for article in articles:
    title = article['title']
    titles.append(title)
print(titles)
#print(articles)

nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()
for title in titles:
    scores = analyzer.polarity_scores(title)
    print(title)
    print(scores)