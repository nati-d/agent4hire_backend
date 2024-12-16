import requests
import os
from typing import List, Optional, Dict, Any

class ECBExchangeRatesAPI:
    """
    A class to interact with the ECB Exchange Rates API.

    Attributes:
        base_url (str): The base URL for the ECB Exchange Rates API.
        api_key (str): The API key for authenticating requests.
    """

    def __init__(self) -> None:
        """
        Initializes the ECBExchangeRatesAPI with base URL and API key.
        """
        self.base_url = "https://api.exchangeratesapi.io/" 
        self.api_key = os.getenv("ECB_API_KEY")  # Get API key from environment variable

    def get_supported_symbols(self) -> Dict[str, Any]:
        """
        Retrieves a list of supported currency symbols from the API.

        Returns:
            Dict[str, Any]: A dictionary containing supported currency symbols.
        """
        response = requests.get(f"{self.base_url}symbols", params={"access_key": self.api_key})
        return response.json()

    def get_latest_rates(self, base_currency: str = 'EUR', symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Retrieves the latest exchange rates for a given base currency.

        Args:
            base_currency (str): The base currency to retrieve rates for. Defaults to 'EUR'.
            symbols (Optional[List[str]]): A list of currency symbols to filter the results. If None, all symbols are returned.

        Returns:
            Dict[str, Any]: A dictionary containing the latest exchange rates.
        """
        params = {'access_key': self.api_key, 'base': base_currency}
        if symbols:
            params['symbols'] = ','.join(symbols)
        response = requests.get(f"{self.base_url}latest", params=params)
        return response.json()

    def get_historical_rates(self, date: str, base_currency: str = 'EUR', symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Retrieves historical exchange rates for a specified date.

        Args:
            date (str): The date for which to retrieve exchange rates (format: YYYY-MM-DD).
            base_currency (str): The base currency to retrieve rates for. Defaults to 'EUR'.
            symbols (Optional[List[str]]): A list of currency symbols to filter the results.

        Returns:
            Dict[str, Any]: A dictionary containing the historical exchange rates.
        """
        params = {'access_key': self.api_key, 'base': base_currency}
        if symbols:
            params['symbols'] = ','.join(symbols)
        response = requests.get(f"{self.base_url}{date}", params=params)
        return response.json()

    def convert_currency(self, from_currency: str, to_currency: str, amount: float, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Converts a specified amount from one currency to another.

        Args:
            from_currency (str): The currency to convert from.
            to_currency (str): The currency to convert to.
            amount (float): The amount to convert.
            date (Optional[str]): The date for historical conversion (format: YYYY-MM-DD). If None, uses the latest rates.

        Returns:
            Dict[str, Any]: A dictionary containing the conversion result.
        """
        params = {
            'access_key': self.api_key,
            'from': from_currency,
            'to': to_currency,
            'amount': amount
        }
        if date:
            params['date'] = date
        response = requests.get(f"{self.base_url}convert", params=params)
        return response.json()

    def get_time_series(self, start_date: str, end_date: str, base_currency: str = 'EUR', symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Retrieves the exchange rates time series for a specified date range.

        Args:
            start_date (str): The start date of the time series (format: YYYY-MM-DD).
            end_date (str): The end date of the time series (format: YYYY-MM-DD).
            base_currency (str): The base currency to retrieve rates for. Defaults to 'EUR'.
            symbols (Optional[List[str]]): A list of currency symbols to filter the results.

        Returns:
            Dict[str, Any]: A dictionary containing the time series exchange rates.
        """
        params = {
            'access_key': self.api_key,
            'start_date': start_date,
            'end_date': end_date,
            'base': base_currency
        }
        if symbols:
            params['symbols'] = ','.join(symbols)
        response = requests.get(f"{self.base_url}timeseries", params=params)
        return response.json()

    def get_fluctuation(self, start_date: str, end_date: str, base_currency: str = 'EUR', symbols: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Retrieves the fluctuation of exchange rates for a specified date range.

        Args:
            start_date (str): The start date of the fluctuation period (format: YYYY-MM-DD).
            end_date (str): The end date of the fluctuation period (format: YYYY-MM-DD).
            base_currency (str): The base currency to retrieve rates for. Defaults to 'EUR'.
            symbols (Optional[List[str]]): A list of currency symbols to filter the results.

        Returns:
            Dict[str, Any]: A dictionary containing the fluctuation of exchange rates.
        """
        params = {
            'access_key': self.api_key,
            'start_date': start_date,
            'end_date': end_date,
            'base': base_currency
        }
        if symbols:
            params['symbols'] = ','.join(symbols)
        response = requests.get(f"{self.base_url}fluctuation", params=params)
        return response.json()
