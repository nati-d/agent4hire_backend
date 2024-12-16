import requests
from typing import Any, Dict, List, Union

class HumanAPI:
    """
    A class to interact with the Human API to aggregate health data from various sources,
    such as fitness trackers and Electronic Health Records (EHRs).
    """

    BASE_URL = "https://api.humanapi.co/v1"  # Replace with actual Human API endpoint if different

    def __init__(self, access_token: str):
        """
        Initializes the HumanAPI client with an access token.

        Args:
            access_token (str): The access token for authenticating requests.
        """
        self.access_token = access_token

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """
        Helper method to make a GET request to the Human API.

        Args:
            endpoint (str): The endpoint to request.

        Returns:
            Dict[str, Any]: The response data as a JSON dictionary.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.BASE_URL}{endpoint}", headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_user_profile(self) -> Dict[str, Any]:
        """
        Fetch the user's profile data.

        Returns:
            Dict[str, Any]: The user profile information.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        endpoint = "/profile"
        return self._make_request(endpoint)

    def get_fitness_data(self) -> Dict[str, Any]:
        """
        Fetch aggregated fitness data from various sources.

        Returns:
            Dict[str, Any]: The aggregated fitness data.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        endpoint = "/fitness"
        return self._make_request(endpoint)

    def get_health_data(self) -> Dict[str, Any]:
        """
        Fetch aggregated health data, including EHR data.

        Returns:
            Dict[str, Any]: The aggregated health data.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        endpoint = "/health"
        return self._make_request(endpoint)
