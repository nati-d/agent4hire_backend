import requests

class BinanceAPI:
    BASE_URL = "https://api.binance.com/api/v3"

    @staticmethod
    def get_ticker_price(symbol: str = None):
        """
        Get the latest price for a specific symbol or all symbols.
        
        :param symbol: The trading pair symbol (e.g., 'BTCUSDT'). If None, returns all symbols.
        :return: JSON response with latest prices.
        """
        endpoint = f"{BinanceAPI.BASE_URL}/ticker/price"
        params = {'symbol': symbol} if symbol else {}
        response = requests.get(endpoint, params=params)
        return response.json()

    @staticmethod
    def get_order_book(symbol: str):
        """
        Get the order book depth for a specific symbol.
        
        :param symbol: The trading pair symbol (e.g., 'BTCUSDT').
        :return: JSON response with order book depth.
        """
        endpoint = f"{BinanceAPI.BASE_URL}/depth"
        params = {'symbol': symbol}
        response = requests.get(endpoint, params=params)
        return response.json()

    @staticmethod
    def get_recent_trades(symbol: str):
        """
        Get recent trades for a specific symbol.
        
        :param symbol: The trading pair symbol (e.g., 'BTCUSDT').
        :return: JSON response with recent trades.
        """
        endpoint = f"{BinanceAPI.BASE_URL}/trades"
        params = {'symbol': symbol}
        response = requests.get(endpoint, params=params)
        return response.json()

    @staticmethod
    def get_historical_trades(symbol: str):
        """
        Get older trades for a specific symbol.
        
        :param symbol: The trading pair symbol (e.g., 'BTCUSDT').
        :return: JSON response with historical trades.
        """
        endpoint = f"{BinanceAPI.BASE_URL}/historicalTrades"
        params = {'symbol': symbol}
        response = requests.get(endpoint, params=params)
        return response.json()

    @staticmethod
    def get_candlestick_data(symbol: str, interval: str):
        """
        Get candlestick data for a specific symbol.
        
        :param symbol: The trading pair symbol (e.g., 'BTCUSDT').
        :param interval: The interval for candlesticks (e.g., '1h').
        :return: JSON response with candlestick data.
        """
        endpoint = f"{BinanceAPI.BASE_URL}/klines"
        params = {'symbol': symbol, 'interval': interval}
        response = requests.get(endpoint, params=params)
        return response.json()

    @staticmethod
    def get_exchange_info():
        """
        Get current exchange trading rules and symbol information.
        
        :return: JSON response with exchange information.
        """
        endpoint = f"{BinanceAPI.BASE_URL}/exchangeInfo"
        response = requests.get(endpoint)
        return response.json()