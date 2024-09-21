#https://levelup.gitconnected.com/python-and-llm-for-market-analysis-part-iii-allow-your-trading-system-to-react-for-daily-news-3310b073af8d

import streamlit as st
from newsapi import NewsApiClient
import datetime
import pandas as pd

class NewsApi:
    def __init__(self):
        self.token = st.secrets.newsapi.api_key
        self.country = "us"
        self.language = "en"
        self.category = "business"      #businessentertainmentgeneralhealthsciencesportstechnology
        self.csv_location = "./data/"
        self.todaydate = datetime.date.today()
        self.filename = f"news_{self.todaydate}.csv"
        self.client = NewsApiClient(api_key=self.token)
    
    def extract_news(self):
        page = 1
        total_news_count = 0
        all_articles = []
        try:
            while True:
                top_headlines = self.client.get_top_headlines(country=self.country, language=self.language, category=self.category, page=page)
                if top_headlines.get("status") == 'ok':
                    for row in top_headlines.get("articles", None):
                        article = [row['publishedAt'], row['title'], row['description'], row['url']]
                        all_articles.append(article)
                page+=1

                if len(all_articles) >= top_headlines['totalResults']:
                    break
            self.all_articles = pd.DataFrame(data=all_articles, columns=['Date','Title','Description','URL'])
            self.all_articles.to_csv(f"{self.csv_location}{self.filename}")
        except Exception as e:
            print(e)


