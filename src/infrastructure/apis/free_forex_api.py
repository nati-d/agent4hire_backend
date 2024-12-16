import requests
from enum import Enum
from typing import Dict, Any, List
import os  # Add this import at the top of the file

class CurrencyPair(Enum):
    """
    Enum representing the supported currency pairs for the Forex API.
    """
    EUR = "EUR"
    GBP = "GBP"
    CAD = "CAD"
    PLN = "PLN"
    USD = "USD"

class FreeForexAPI:
    """
    Class to interact with the Forex API to fetch real-time foreign exchange rates.
    """
    BASE_URL = "http://apilayer.net/api/live"

    def __init__(self) -> None:  # Update the parameter to have a default value
        """
        Initializes the FreeForexAPI instance with the access key.

        :param access_key: Your access key for the API. If not provided, it will be loaded from the environment variable.
        """
        self.access_key = os.getenv('FOREX_API_ACCESS_KEY')

    def get_exchange_rates(self, currencies: List[CurrencyPair], source: CurrencyPair = CurrencyPair.USD) -> Dict[str, Any]:
        """
        Fetches the exchange rates for given currencies with respect to the source currency.

        :param currencies: A list of CurrencyPair enum instances representing the currencies to fetch.
        :param source: An instance of CurrencyPair enum representing the source currency (default is USD).
        :return: A dictionary containing the exchange rate data.
        :raises ValueError: If the response format is unexpected.
        :raises requests.exceptions.RequestException: For network-related errors.
        """
        # Prepare the currencies parameter as a comma-separated string
        currencies_str = ",".join(currency.value for currency in currencies)
        
        # Prepare the request URL
        params = {
            'access_key': self.access_key,
            'currencies': currencies_str,
            'source': source.value,
            'format': 1
        }
        
        response = requests.get(self.BASE_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            if 'quotes' in data:
                return data['quotes']
            else:
                raise ValueError("Unexpected response format: 'quotes' key not found")
        else:
            response.raise_for_status()
