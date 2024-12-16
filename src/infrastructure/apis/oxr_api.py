import requests
import os

class OpenExchangeRatesClient:
    BASE_URL = "https://openexchangerates.org/api/"

    def __init__(self, api_key=None):
        """
        Initialize the client with an API key.
        If no API key is provided, it will try to get it from the environment variable 'OPENEXCHANGE_API_KEY'.
        """
        self.api_key = api_key or os.getenv("OPENEXCHANGE_API_KEY")
        
    def fetch_latest_rates(self, base="USD"):
        """
        Fetch the latest exchange rates with the specified base currency.
        
        :param base: The base currency for the exchange rates (default is "USD").
        :return: A dictionary containing the latest exchange rates.
        """
        params = {
            "app_id": self.api_key,
            "base": base
        }
        response = requests.get(f"{self.BASE_URL}latest.json", params=params)
        return response.json()

    def fetch_historical_rates(self, date, base="USD"):
        """
        Fetch historical exchange rates for a specific date with the specified base currency.
        
        :param date: The date for the historical rates in the format 'YYYY-MM-DD'.
        :param base: The base currency for the exchange rates (default is "USD").
        :return: A dictionary containing the historical exchange rates for the specified date.
        """
        params = {
            "app_id": self.api_key,
            "base": base
        }
        response = requests.get(f"{self.BASE_URL}historical/{date}.json", params=params)
        return response.json()