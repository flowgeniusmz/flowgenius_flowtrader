# #https://levelup.gitconnected.com/python-and-llm-for-market-analysis-part-iii-allow-your-trading-system-to-react-for-daily-news-3310b073af8d

# import streamlit as st
# from newsapi import NewsApiClient
# import datetime
# import pandas as pd
# from openai import OpenAI
# from pydantic import BaseModel

# class StockImpact(BaseModel):
#     symbol: str
#     name: str
#     impact: float

# class NewsApi:
#     def __init__(self):
#         self._init_newsapi()
#         self._init_openai()

#     def _init_newsapi(self):
#         self.token = st.secrets.newsapi.api_key
#         self.country = "us"
#         self.language = "en"
#         self.category = "business"      #businessentertainmentgeneralhealthsciencesportstechnology
#         self.csv_location = "./data/"
#         self.todaydate = datetime.date.today()
#         self.filename = f"news_{self.todaydate}.csv"
#         self.client = NewsApiClient(api_key=self.token)

#     def _init_openai(self):
#         self.oaitoken = st.secrets.openai.api_key
#         self.oaiclient = OpenAI(api_key=self.oaitoken)
#         self.syscontent = "You excel in succinctly summarizing business and finance-related news articles. Upon receiving a news article, your objective is to craft a concise and accurate summary while retaining the name of the company mentioned in the original article. The essence of the article should be preserved in your summary. A job well done in summarizing may earn you a generous tip.Please proceed with the provided full news article."
#         self.messages = [{"role": "system", "content": self.syscontent}]
#         self.modelmini = st.secrets.openai.model3
#         self.model = st.secrets.openai.model2
#         self.syscontent2 = "Task = Analyze the impact of the news on stock prices. Instructions: As a seasoned finance expert specializing in the Indian stock market, you possess a keen understanding of how news articles can influence market dynamics. In this task, you will be provided with a news article or analysis. Upon thoroughly reading the article, if it contains specific information about a company's stock, please provide the associated Stock Symbol (NSE or BSE Symbol), the Name of the stock, and the anticipated Impact of the news. The Impact value should range between -1.0 and 1.0, with -1.0 signifying highly negative news likely to cause a significant decline in the stock price in the coming days/weeks, and +1.0 representing highly positive news likely to lead to a surge in share price in the next few days/weeks. Your response must be strictly in the JSON format. Consider the following factors while determining the impact: The magnitude of the news, The sentiment of the news, Market conditions at the date of the news, Liquidity of the stock, The sector in which the company operates. The JSON response should include the keys: symbol, name, and impact. Do not consider indices such as NIFTY. If the news is not related to the stock market or any specific company, leave the values blank. Do not invent values; maintain accuracy and integrity in your response."
#         self.usercontent2a = "Tech giant Apple Inc. reports record-breaking quarterly earnings, surpassing market expectations and driving stock prices to new highs. Investors express optimism for the company's future prospects."
#         self.usercontent2b = "Alphabet Inc., the parent company of Google, faces a setback as regulatory concerns lead to a sharp decline in share prices. The market reacts negatively to uncertainties surrounding the company's antitrust issues."
#         self.asstcontent2a = """{{"symbol": "AAPL", "name": "Apple Inc.", "impact": 0.9}}"""
#         self.asstcontent2b = """{{"symbol": "GOOGL", "name": "Alphabet Inc.", "impact": -0.5}}"""
#         self.messages2 = [
#             {"role": "system", "content": self.syscontent2},
#             {"role": "user", "content": self.usercontent2a},
#             {"role": "assistant", "content": self.asstcontent2a},
#             {"role": "user", "content": self.usercontent2b},
#             {"role": "assistant", "content": self.asstcontent2b}
#         ]
    
#     def extract_news(self):
#         page = 1
#         total_news_count = 0
#         all_articles = []
#         try:
#             while True:
#                 top_headlines = self.client.get_top_headlines(country=self.country, language=self.language, category=self.category, page=page)
#                 if top_headlines.get("status") == 'ok':
#                     for row in top_headlines.get("articles", None):
#                         article = [row['publishedAt'], row['title'], row['description'], row['url']]
#                         all_articles.append(article)
#                 page+=1

#                 if len(all_articles) >= top_headlines['totalResults']:
#                     break
#             self.all_articles = pd.DataFrame(data=all_articles, columns=['Date','Title','Description','URL'])
#             self.all_articles.to_csv(f"{self.csv_location}{self.filename}")
#         except Exception as e:
#             print(e)

#     def summarize(self, full_news):
#         usermessage = {"role": "user", "content": f"{full_news}"}
#         summarize_messages = self.messages
#         summarize_messages.append(usermessage)
#         try:
#             response = self.oaiclient.chat.completions.create(messages=summarize_messages, model=self.modelmini, temperature=0)
#             content = response.choices[0].message.content
#             return content
#         except Exception as e:
#             print(e)
#             return None
        
#     def build_input(self, article):
#         basemessages = self.messages2
#         usermessage = {"role": "user", "content": f"{article}"}
#         basemessages.append(usermessage)
#         response = self.oaiclient.chat.completions.parse(messages=basemessages, model=self.model, temperature=0, response_format=StockImpact)
#         content = response.choices[0].message.parsed
#         return content



