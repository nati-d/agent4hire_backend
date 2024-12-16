import os
import requests
from flask import current_app
from dotenv import load_dotenv

class CoinloreAPI:
    """
    CoinloreAPI is a class for interacting with the Coinlore API, providing methods to get cryptocurrency data.

    Attributes:
        base_url (str): The base URL for Coinlore API endpoints.

    Methods:
        get_global_data() -> dict:
            Gets global cryptocurrency statistics.

        get_tickers(start: int = 0, limit: int = 100) -> dict:
            Gets tick data for multiple cryptocurrencies.

        get_ticker(coin_id: int) -> dict:
            Gets tick data for a specific cryptocurrency.

        get_markets_for_coin(coin_id: int) -> dict:
            Gets top exchanges and markets for a specific cryptocurrency.

        get_all_exchanges() -> dict:
            Gets all exchanges listed on the platform.

        get_exchange(exchange_id: int) -> dict:
            Gets specific exchange data using its ID.

        get_social_stats(coin_id: int) -> dict:
            Gets social stats for a specific cryptocurrency.
    """
    
    BASE_URL = "https://api.coinlore.net/api"
    
    def __init__(self):
        """Initializes the CoinloreAPI class."""
        load_dotenv()  # Load environment variables from .env file if needed

    def _make_request(self, endpoint: str, params: dict = None) -> dict:
        """
        Helper method to make a GET request to the Coinlore API.
        
        :param endpoint: The API endpoint to call.
        :param params: Optional dictionary of query parameters for the request.
        :return: A dictionary containing the API response.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            current_app.logger.error(f"Error making Coinlore API call: {str(e)}")
            return {}

    def get_global_data(self) -> dict:
        """Get global cryptocurrency statistics."""
        return self._make_request("global/")

    def get_tickers(self, start: int = 0, limit: int = 100) -> dict:
        """Get tick data for multiple cryptocurrencies."""
        return self._make_request("tickers/", {"start": start, "limit": limit})

    def get_ticker(self, coin_id: int) -> dict:
        """Get tick data for a specific cryptocurrency."""
        return self._make_request("ticker/", {"id": coin_id})

    def get_markets_for_coin(self, coin_id: int) -> dict:
        """Get top exchanges and markets for a specific cryptocurrency."""
        return self._make_request("coin/markets/", {"id": coin_id})

    def get_all_exchanges(self) -> dict:
        """Get all exchanges listed on the platform."""
        return self._make_request("exchanges/")

    def get_exchange(self, exchange_id: int) -> dict:
        """Get specific exchange data using its ID."""
        return self._make_request("exchange/", {"id": exchange_id})

    def get_social_stats(self, coin_id: int) -> dict:
        """Get social stats for a specific cryptocurrency."""
        return self._make_request("coin/social_stats/", {"id": coin_id})


# Example usage:
if __name__ == "__main__":
    api = CoinloreAPI()

    # Get global data
    global_data = api.get_global_data()
    print("Global Data:")
    print(global_data)

    # Get tickers (first 100 coins)
    tickers = api.get_tickers()
    print("\nTickers (First 100 Coins):")
    print(tickers)

    # Get specific coin data (e.g., Bitcoin with ID 90)
    bitcoin_data = api.get_ticker(90)
    print("\nBitcoin Data:")
    print(bitcoin_data)

    # Get markets for Bitcoin
    bitcoin_markets = api.get_markets_for_coin(90)
    print("\nBitcoin Markets:")
    print(bitcoin_markets)

    # Get all exchanges
    exchanges = api.get_all_exchanges()
    print("\nAll Exchanges:")
    print(exchanges)

    # Get specific exchange data (e.g., Binance with ID 5)
    binance_data = api.get_exchange(5)
    print("\nBinance Data:")
    print(binance_data)

    # Get social stats for Bitcoin
    bitcoin_social_stats = api.get_social_stats(90)
    print("\nBitcoin Social Stats:")
    print(bitcoin_social_stats)
