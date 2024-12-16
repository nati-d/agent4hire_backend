import requests
from typing import Any, Dict, List

class CDCAPI:
    """
    A class to interact with the CDC APIs to access public health data and statistics
    from the Centers for Disease Control and Prevention.
    """

    def __init__(self):
        """
        Initializes the CDCAPI client with configurable base URLs.
        """
        self.BASE_URL_OPEN_DATA = "https://data.cdc.gov"
        self.BASE_URL_PHIN_VADS = "http://phinvads.cdc.gov/vocabService/v2"
        self.BASE_URL_WONDER = "https://wonder.cdc.gov/controller/datarequest"
        self.BASE_URL_CONTENT_SYNDICATION = "https://tools.cdc.gov/api/v2"

    def _make_request(self, url: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Helper method to make a GET request to the specified URL.

        Args:
            url (str): The API endpoint to request.
            params (Dict[str, Any], optional): Query parameters to include in the request.

        Returns:
            Dict[str, Any]: The response data as a JSON dictionary.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_open_data(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch open data from the CDC Open Data API.

        Args:
            params (Dict[str, Any], optional): Additional query parameters.

        Returns:
            List[Dict[str, Any]]: A list of open data records.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.BASE_URL_OPEN_DATA}/api/views.json"
        return self._make_request(url, params)

    def get_phin_vads(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch standard vocabularies from the PHIN VADS API.

        Args:
            params (Dict[str, Any], optional): Additional query parameters.

        Returns:
            List[Dict[str, Any]]: A list of vocabularies.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.BASE_URL_PHIN_VADS}/vocabService/v2"
        return self._make_request(url, params)

    def get_wonder_data(self, database_id: str) -> Dict[str, Any]:
        """
        Access data from the WONDER API using the specified database ID.

        Args:
            database_id (str): The ID of the database to query.

        Returns:
            Dict[str, Any]: The requested data in XML format.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.BASE_URL_WONDER}/{database_id}"
        return self._make_request(url)

    def get_content_syndication(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Fetch content syndication data from the CDC Content Syndication API.

        Args:
            params (Dict[str, Any], optional): Additional query parameters.

        Returns:
            Dict[str, Any]: A dictionary of content syndication records.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = self.BASE_URL_CONTENT_SYNDICATION
        return self._make_request(url, params)

    def get_tracking_network_data(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch data from the Environmental Public Health Tracking Network API.

        Args:
            params (Dict[str, Any], optional): Additional query parameters.

        Returns:
            List[Dict[str, Any]]: A list of tracking network records.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = self.BASE_URL_TRACKING_NETWORK
        return self._make_request(url, params)
