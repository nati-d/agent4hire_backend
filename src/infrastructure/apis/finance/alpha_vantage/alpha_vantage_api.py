import requests
import os

class AlphaVantageClient:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")

    def fetch_stock_daily(self, symbol):
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()

    def fetch_forex_rate(self, from_currency, to_currency):
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_currency,
            "to_currency": to_currency,
            "apikey": self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()

    def fetch_sma(self, symbol, interval="daily", time_period=10):
        params = {
            "function": "SMA",
            "symbol": symbol,
            "interval": interval,
            "time_period": time_period,
            "series_type": "close",
            "apikey": self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()

    def fetch_crypto_exchange_rate(self, from_currency, to_currency):
        params = {
            "function": "CURRENCY_EXCHANGE_RATE",
            "from_currency": from_currency,
            "to_currency": to_currency,
            "apikey": self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()

    def fetch_intraday_stock(self, symbol, interval="5min"):
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "apikey": self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        return response.json()



