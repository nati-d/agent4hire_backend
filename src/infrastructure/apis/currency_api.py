from typing import Dict, Optional
import currencyapicom


class CurrencyAPI:
    """
    CurrencyAPI class is a class for interacting with the CurrencyAPI, providing methods to get exchange rate data,
    both current and historical.

    Attributes:
        base_url (str): The base URL for CurrencyAPI endpoints.

    Methods:
        get_status() -> Dict:
            A disctionary containing the API response.

        get_currencies(currencies, type) -> Dict:
            A dictionary with the list of all the currencies.

        get_latest_exchange_rates(base_currency, currencies, type) -> Dict:
            A dictionary containing the latest exchange raters.

        get_historical_exchange_rates(date, base_currency, type, currencies) -> Dict:
            A dictionary historical exchange rates for a specific date

        get_range_historical_exchange_rates(datetime_start, datetime_end, base_currency, accuracy, type, currencies) -> Dict:
            A dictionary of the historical exchange rates for a specified date range.

        get_convert_exchange_rates(value, date, base_currency, currencies, type) -> Dict:
            A dictionary containing the calculated values for today or any given date for all currencies.
    """

    def __init__(self, api_key: str):
        self.client = currencyapicom.Client(api_key)

    def get_status(self) -> Dict:
        """
        This status endpoint returns information about your current quota.

        :return: A dictionary containing the API response.
        """

        return self.client.status()

    def get_currencies(
        self,
        currencies: Optional[str] = None,
        type: Optional[str] = None,
    ) -> Dict:
        """
        This endpoint returns a list of all available currencies.

        :param currencies: An optional list of comma seperated currency codes which you want to get (EUR,USD,CAD)
        By default all available currencies will be shown.

        :param type: An optional type of currency you want to get (fiat, metal or crypto) By default all types will be shown.

        :return: A dictionary containing the API response.
        """

        params = {"currencies": currencies, "type": type}
        filtered_params = {k: v for k, v in params.items() if v is not None}

        return self.client.currencies(**filtered_params)

    def get_latest_exchange_rates(
        self,
        base_currency: str = "USD",
        currencies: Optional[str] = None,
        type: Optional[str] = None,
    ) -> Dict:
        """
        This endpoint returns the latest exchange rates.

        :param base: The base currency code, by default USD.
        :param currencies: A list of comma-separated currency codes which you want to get (EUR,USD,CAD)
        :param type: An optional type of currency you want to get (fiat, metal or crypto) By default all types will be shown.

        :return: A dictionary containing the API response.
        """

        params = {"base": base_currency, "currencies": currencies, "type": type}
        filtered_params = {k: v for k, v in params.items() if v is not None}

        return self.client.latest(**filtered_params)

    def get_historical_exchange_rates(
        self,
        date: str,
        base_currency: str = "USD",
        type: Optional[str] = None,
        currencies: Optional[str] = None,
    ) -> Dict:
        """
        This endpoint returns historical exchange rates for a specific date.

        :param date: The date for which you want to get the exchange rates (format:YYYY-MM-DD).
        :param base_currency: The base currency code, by default USD.
        :param type: An optional type of currency you want to get (fiat, metal or crypto) By default all types will be shown.
        :param currencies: A list of comma-separated currency codes which you want to get (EUR,USD,CAD), by default all available currencies will be shown.

        :return: A dictionary containing the API response.
        """

        params = {
            "date": date,
            "base": base_currency,
            "currencies": currencies,
            "type": type,
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}

        return self.client.historical(**filtered_params)

    def get_range_historical_exchange_rates(
        self,
        datetime_start: str,
        datetime_end: str,
        base_currency: str = "USD",
        accuracy: str = "day",
        type: Optional[str] = None,
        currencies: Optional[str] = None,
    ) -> Dict:
        """
        This historical exchange rates endpoint provides currency rates for a specified date range.

        :param datetime_start: Datetime for the start of your requested range (format: 2022-12-01T00:00:00Z / ISO8601 Datetime)
        :param datetime_end: Datetime for the end of your requested range (format: 2022-12-01T00:00:00Z / ISO8601 Datetime)

        Optional parameters:
        :param accuracy: The accuracy you want to receive. Possible Values: day, hour, quarter_hour, minute Default: day For valid time ranges see below
        :param base_currency: The base currency to which all results are behaving relative to By default all values are based on USD
        :param currencies: A list of comma-separated currency codes which you want to get (EUR,USD,CAD), by default all available currencies will be shown.
        :param type: An optional type of currency you want to get (fiat, metal or crypto) By default all types will be shown.

        Valid Accuracy Time Ranges

        day
            - not more than 366 days back

        hour
            - not more than 7 days between start and end
            - not more than 3 months back

        quarter_hour
            - not more than 24 hours between start and end
            - not more than 7 days back

        minute
            - not more than 6 hours between start and end
            - not more than 7 days back
        """

        params = {
            "accuracy": accuracy,
            "base_currency": base_currency,
            "currencies": currencies,
            "type": type,
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}

        return self.client.range(datetime_start, datetime_end, **filtered_params)

    def convert_exchange_rates(
        self,
        value: str,
        date: Optional[str] = None,
        base_currency: str = "USD",
        currencies: Optional[str] = None,
        type: Optional[str] = None,
    ) -> Dict:
        """
        Returns calculated values for today or any given date for all currencies.

        :param value: The value you want to convert

        Optional attributes
        :param date: Date to retrieve historical rates from (format: 2021-12-31).
        :param base_currency: The base currency to which all results are behaving relative to By default all values are based on USD.
        :param currencies: A list of comma seperated currency codes which you want to get (EUR,USD,CAD) By default all available currencies will be shown.
        :param type: They type of currency you want to get (fiat, metal or crypto) By default all types will be shown.
        """

        params = {
            "date": date,
            "base_currency": base_currency,
            "currencies": currencies,
            "type": type,
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}

        return self.client.convert(value, **filtered_params)


if __name__ == "__main__":
    api_key = "ADD API KEY HERE"
    currency_api = CurrencyAPI(api_key)

    # print(currency_api.get_status())
    """
    Sample Response:

    {
        'account_id': 382496707935604736,
        'quotas': {
            'month': {
                'total': 300,
                'used': 0,
                'remaining': 300
            },
            'grace': {
                'total': 0,
                'used': 0,
                'remaining': 0
            }
        }
    }
    """

    # print(currency_api.get_currencies())
    """
    Sample Response:

    {
        'data': {
            'AED': {'
                symbol': 'AED',
                'name': 'United Arab Emirates Dirham',
                'symbol_native': 'د.إ',
                'decimal_digits': 2,
                'rounding': 0,
                'code': 'AED',
                'name_plural':
                'UAE dirhams',
                'type': 'fiat',
                'countries': ['AE']
            },
            'AFN': {
                'symbol': 'Af',
                'name': 'Afghan Afghani',
                'symbol_native': '؋',
                'decimal_digits': 0,
                'rounding': 0,
                'code': 'AFN',
                'name_plural': 'Afghan Afghanis',
                'type': 'fiat',
                'countries': ['AF']
            },
        }
    }

    """

    # print(currency_api.get_latest_exchange_rates())

    # print(currency_api.get_historical_exchange_rates("2022-01-01"))

    # print(currency_api.get_range_historical_exchange_rates("2022-01-01T00:00:00Z", "2022-01-02T00:00:00Z"))
