import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
import streamlit as st
import pandas as pd


# ###1
# nltk.download("vader_lexicon")
# analyzer = SentimentIntensityAnalyzer()


# # List of example texts to analyze
# texts = [
#     "I love this product! It works great and is very affordable.",
#     "This product is okay. It gets the job done, but could be better.",
#     "I hate this product. It doesn't work at all and is a waste of money."
# ]

# # Loop through the texts and get the sentiment scores for each one
# for text in texts:
#     scores = analyzer.polarity_scores(text)
#     print(text)
#     print(scores)

### 2
newsClient = NewsApiClient(api_key=st.secrets.newsapi.api_key)
top_headlines = newsClient.get_top_headlines(q="tesla") #, category="business", language="en", country="us")
print(top_headlines)