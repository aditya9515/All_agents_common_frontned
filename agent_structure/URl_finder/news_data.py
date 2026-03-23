import os
from newsapi import NewsApiClient


def news_api_data(query: str):
    api_key = os.getenv("NEWS_API")
    if not api_key:
        api_key = "e5fdbe1548614432a26b4f47b2e7f29f"
    clinet = NewsApiClient(api_key=api_key)
    articles = clinet.get_everything(
        q=query,
        language="en",
        sort_by="relevancy"
    )
    
    return articles
