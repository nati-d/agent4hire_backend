import requests
import os
from dotenv import load_dotenv
from typing import Any, Dict, List

# Load environment variables from .env file
load_dotenv()

class OpenFDAAPI:
    """
    A class to interact with the OpenFDA API to access public FDA data,
    including drug, device, and food information.
    """

    BASE_URL = "https://api.fda.gov"

    def __init__(self):
        """
        Initializes the OpenFDAAPI client.

        Args:
            api_key (str, optional): The API key for increased request limits.
        """
        self.api_key = os.getenv("OPEN_FDA_API_KEY")  # Load from .env if not provided

    def _make_request(self, endpoint: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Helper method to make a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to request.
            params (Dict[str, Any], optional): Query parameters to include in the request.

        Returns:
            Dict[str, Any]: The response data as a JSON dictionary.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = {}
        if self.api_key:
            headers['User-Agent'] = self.api_key
        
        response = requests.get(f"{self.BASE_URL}{endpoint}", headers=headers, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_drugs(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch drug information from the OpenFDA API.

        Args:
            params (Dict[str, Any], optional): Additional query parameters.

        Returns:
            List[Dict[str, Any]]: A list of drug records.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        endpoint = "/drugs.json"
        return self._make_request(endpoint, params)

    def get_devices(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch medical device information from the OpenFDA API.

        Args:
            params (Dict[str, Any], optional): Additional query parameters.

        Returns:
            List[Dict[str, Any]]: A list of device records.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        endpoint = "/devices.json"
        return self._make_request(endpoint, params)

    def get_foods(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Fetch food information from the OpenFDA API.

        Args:
            params (Dict[str, Any], optional): Additional query parameters.

        Returns:
            List[Dict[str, Any]]: A list of food records.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        endpoint = "/food.json"
        return self._make_request(endpoint, params)
