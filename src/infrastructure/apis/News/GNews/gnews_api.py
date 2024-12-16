import requests
import os

class GNewsClient:
    BASE_URL = "https://gnews.io/api/v4/"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GNEWS_API_KEY")
        
    def fetch_news_by_category(self, category, lang="en"):
        params = {
            "token": self.api_key,
            "topic": category,
            "lang": lang
        }
        response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
        return response.json()

    def fetch_top_headlines(self, lang="en"):
        params = {
            "token": self.api_key,
            "lang": lang
        }
        response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
        return response.json()

    def fetch_technology_news(self, lang="en"):
        params = {
            "token": self.api_key,
            "topic": "technology",
            "lang": lang
        }
        response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
        return response.json()

    def fetch_topic_news(self, topic, lang="en"):
        params = {
            "token": self.api_key,
            "topic": topic,
            "lang": lang
        }
        response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
        return response.json()

    def search_news(self, query, lang="en"):
        params = {
            "token": self.api_key,
            "q": query,
            "lang": lang
        }
        response = requests.get(f"{self.BASE_URL}search", params=params)
        return response.json()

    def fetch_news_by_country(self, country, lang="en"):
        params = {
            "token": self.api_key,
            "country": country,
            "lang": lang
        }
        response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
        return response.json()

    def fetch_news_by_language(self, lang):
        params = {
            "token": self.api_key,
            "lang": lang
        }
        response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
        return response.json()

    def fetch_news_by_source(self, source, lang="en"):
        params = {
            "token": self.api_key,
            "lang": lang,
            "sources": source
        }
        response = requests.get(f"{self.BASE_URL}top-headlines", params=params)
        return response.json()

    def search_news(self, query, lang="en"):
        params = {
            "token": self.api_key,
            "q": query,
            "lang": lang
        }
        response = requests.get(f"{self.BASE_URL}search", params=params)
        return response.json()

