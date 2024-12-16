from enum import Enum
from typing import Dict, Optional, Any
import requests
import os  # Import os module to access environment variables

class CryptoCompareEndpoint(Enum):
    PRICE = "price"
    HISTO_MINUTE = "histominute"
    HISTO_HOUR = "histohour"
    HISTO_DAY = "histoday"
    TOP_BY_VOLUME = "top/totalvolfull"
    COIN_SNAPSHOT = "coinsnapshot"
    
    # latest social
    LATEST_SOCIAL_STATS = "social/coin/latest"
    HISTORICAL_DAY_SOCIAL_STATS = "social/coin/historical/day"
    HISTORICAL_HOUR_SOCIAL_STATS = "social/coin/historical/hour"

    COIN_LIST = "all/coinlist"

    # News endpoints
    NEWS = "v2/news/"
    FEEDS = "news/feeds"
    CATEGORIES = "news/categories"
    FEEDS_AND_CATEGORIES = "news/feedsandcategories"

    # Asset data by symbol
    ASSET_BY_SYMBOL = "asset/v1/data/by/symbol"

class CryptoCompareAPI:
    BASE_URL = "https://min-api.cryptocompare.com/data/"

    def __init__(self):
        """
        Initialize the CryptoCompareAPI with the given API key.
        """
        self.api_key = os.getenv("CRYPTOCOMPARE_API_KEY")  # Get API key from environment variable

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the CryptoCompare API.

        Args:
            endpoint (str): The API endpoint to request.
            params (Optional[Dict[str, Any]]): Optional parameters for the request.

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_price(self, fsym: str, tsyms: str) -> Dict[str, Any]:
        """
        Get the current price of a cryptocurrency.

        Args:
            fsym (str): The cryptocurrency symbol of interest (e.g., BTC).
            tsyms (str): Comma-separated list of target currency symbols (e.g., USD,EUR).

        Returns:
            Dict[str, Any]: The JSON response containing the price.
        """
        endpoint = CryptoCompareEndpoint.PRICE.value
        params = {
            "fsym": fsym,
            "tsyms": tsyms
        }
        return self._get(endpoint, params)

    def get_historical_data(
        self,
        fsym: str,
        tsym: str,
        endpoint: CryptoCompareEndpoint,
        limit: int = 30,
        aggregate: int = 1
    ) -> Dict[str, Any]:
        """
        Get historical data for a cryptocurrency.

        Args:
            fsym (str): The cryptocurrency symbol of interest (e.g., BTC).
            tsym (str): The target currency symbol (e.g., USD).
            endpoint (CryptoCompareEndpoint): The type of historical data (e.g., histominute, histohour, histoday).
            limit (int): The number of data points to retrieve. Default is 30.
            aggregate (int): The aggregation interval in minutes/hours/days. Default is 1.

        Returns:
            Dict[str, Any]: The JSON response containing the historical data.
        """
        params = {
            "fsym": fsym,
            "tsym": tsym,
            "limit": limit,
            "aggregate": aggregate
        }
        return self._get(endpoint.value, params)

    def get_minute_data(self, fsym: str, tsym: str, limit: int = 30, aggregate: int = 1) -> Dict[str, Any]:
        """
        Get historical minute data for a cryptocurrency.

        Args:
            fsym (str): The cryptocurrency symbol of interest (e.g., BTC).
            tsym (str): The target currency symbol (e.g., USD).
            limit (int): The number of data points to retrieve. Default is 30.
            aggregate (int): The aggregation interval in minutes. Default is 1.

        Returns:
            Dict[str, Any]: The JSON response containing the historical minute data.
        """
        return self.get_historical_data(fsym, tsym, CryptoCompareEndpoint.HISTO_MINUTE, limit, aggregate)

    def get_hourly_data(self, fsym: str, tsym: str, limit: int = 30, aggregate: int = 1) -> Dict[str, Any]:
        """
        Get historical hourly data for a cryptocurrency.

        Args:
            fsym (str): The cryptocurrency symbol of interest (e.g., BTC).
            tsym (str): The target currency symbol (e.g., USD).
            limit (int): The number of data points to retrieve. Default is 30.
            aggregate (int): The aggregation interval in hours. Default is 1.

        Returns:
            Dict[str, Any]: The JSON response containing the historical hourly data.
        """
        return self.get_historical_data(fsym, tsym, CryptoCompareEndpoint.HISTO_HOUR, limit, aggregate)

    def get_daily_data(self, fsym: str, tsym: str, limit: int = 30, aggregate: int = 1) -> Dict[str, Any]:
        """
        Get historical daily data for a cryptocurrency.

        Args:
            fsym (str): The cryptocurrency symbol of interest (e.g., BTC).
            tsym (str): The target currency symbol (e.g., USD).
            limit (int): The number of data points to retrieve. Default is 30.
            aggregate (int): The aggregation interval in days. Default is 1.

        Returns:
            Dict[str, Any]: The JSON response containing the historical daily data.
        """
        return self.get_historical_data(fsym, tsym, CryptoCompareEndpoint.HISTO_DAY, limit, aggregate)

    def get_top_by_volume(self, tsym: str, limit: int = 10) -> Dict[str, Any]:
        """
        Get the top cryptocurrencies by total volume.

        Args:
            tsym (str): The target currency symbol (e.g., USD).
            limit (int): The number of top coins to retrieve. Default is 10.

        Returns:
            Dict[str, Any]: The JSON response containing the top coins by volume.
        """
        endpoint = CryptoCompareEndpoint.TOP_BY_VOLUME.value
        params = {
            "tsym": tsym,
            "limit": limit
        }
        return self._get(endpoint, params)

    def get_coin_snapshot(self, fsym: str, tsym: str) -> Dict[str, Any]:
        """
        Get a coin snapshot.

        Args:
            fsym (str): The cryptocurrency symbol of interest (e.g., BTC).
            tsym (str): The target currency symbol (e.g., USD).

        Returns:
            Dict[str, Any]: The JSON response containing the coin snapshot.
        """
        endpoint = CryptoCompareEndpoint.COIN_SNAPSHOT.value
        params = {
            "fsym": fsym,
            "tsym": tsym
        }
        return self._get(endpoint, params)


    def get_latest_social_stats(self, coin_id: str) -> Dict[str, Any]:
        """
        Retrieve the latest social stats for a specific cryptocurrency.

        Args:
            coin_id (str): The ID of the cryptocurrency.

        Returns:
            Dict[str, Any]: The JSON response containing the latest social stats data.
        """
        endpoint = CryptoCompareEndpoint.LATEST_SOCIAL_STATS.value
        params = {"id": coin_id}
        return self._get(endpoint, params)

    def get_historical_day_social_stats(self, coin_id: str, timestamp: int) -> Dict[str, Any]:
        """
        Retrieve historical social stats data for a specific cryptocurrency for a given day.

        Args:
            coin_id (str): The ID of the cryptocurrency.
            timestamp (int): The timestamp for the specific day (in Unix format).

        Returns:
            Dict[str, Any]: The JSON response containing the historical day social stats data.
        """
        endpoint = CryptoCompareEndpoint.HISTORICAL_DAY_SOCIAL_STATS.value
        params = {
            "id": coin_id,
            "ts": timestamp
        }
        return self._get(endpoint, params)

    def get_historical_hour_social_stats(self, coin_id: str, timestamp: int) -> Dict[str, Any]:
        """
        Retrieve historical social stats data for a specific cryptocurrency for a given hour.

        Args:
            coin_id (str): The ID of the cryptocurrency.
            timestamp (int): The timestamp for the specific hour (in Unix format).

        Returns:
            Dict[str, Any]: The JSON response containing the historical hour social stats data.
        """
        endpoint = CryptoCompareEndpoint.HISTORICAL_HOUR_SOCIAL_STATS.value
        params = {
            "id": coin_id,
            "ts": timestamp
        }
        return self._get(endpoint, params)

    def get_coin_list(self) -> Dict[str, Any]:
        """
        Retrieve the complete list of cryptocurrencies.

        Returns:
            Dict[str, Any]: The JSON response containing the list of cryptocurrencies.
        """
        endpoint = CryptoCompareEndpoint.COIN_LIST.value
        return self._get(endpoint)
    
    def get_news(self, lang: str = "EN") -> Dict[str, Any]:
        """
        Retrieve the latest news articles.

        Args:
            lang (str): The language of the news articles. Default is 'EN'.

        Returns:
            Dict[str, Any]: The JSON response containing the latest news articles.
        """
        endpoint = CryptoCompareEndpoint.NEWS.value
        params = {"lang": lang}
        return self._get(endpoint, params)

    def get_feeds(self) -> Dict[str, Any]:
        """
        Retrieve the news feeds.

        Returns:
            Dict[str, Any]: The JSON response containing the news feeds.
        """
        endpoint = CryptoCompareEndpoint.FEEDS.value
        return self._get(endpoint)

    def get_categories(self) -> Dict[str, Any]:
        """
        Retrieve the news categories.

        Returns:
            Dict[str, Any]: The JSON response containing the news categories.
        """
        endpoint = CryptoCompareEndpoint.CATEGORIES.value
        return self._get(endpoint)

    def get_feeds_and_categories(self) -> Dict[str, Any]:
        """
        Retrieve the news feeds and categories.

        Returns:
            Dict[str, Any]: The JSON response containing the news feeds and categories.
        """
        endpoint = CryptoCompareEndpoint.FEEDS_AND_CATEGORIES.value
        return self._get(endpoint)
    
    def get_asset_by_symbol(self, asset_symbol: str) -> Dict[str, Any]:
        """
        Retrieve asset data by symbol.

        Args:
            asset_symbol (str): The symbol of the asset (e.g., 'BTC').

        Returns:
            Dict[str, Any]: The JSON response containing the asset data.
        """
        endpoint = f"{CryptoCompareEndpoint.ASSET_BY_SYMBOL.value}?asset_symbol={asset_symbol}"
        return self._get(endpoint)