import os
import requests
from flask import current_app


class HunterAPI:
    """
    HunterAPI is a class for interacting with the Hunter.io API, providing methods
    to search for email addresses by domain and to find email addresses given a 
    domain and a person's name.

    Attributes:
        api_key (str): The API key for accessing the Hunter.io API, sourced from the Flask app configuration.
        base_url (str): The base URL for the Hunter.io API.

    Methods:
        domain_search(domain: str) -> dict:
            Searches for email addresses associated with the specified domain.

        email_finder(domain: str, first_name: str, last_name: str) -> dict:
            Finds an email address given the domain and a person's first and last name.
    """
    
    def __init__(self):
        """
        Initializes the HunterAPI class by fetching the API key from the environment variables.
        Raises a ValueError if the API key is not found.
        """
        from dotenv import load_dotenv  # Import load_dotenv
        load_dotenv()  # Load environment variables
        self.api_key = os.getenv('HUNTER_API_KEY')  # Use os.getenv to get the API key
        if not self.api_key:
            raise ValueError("Hunter API key not found in the environment variables")
        self.base_url = "https://api.hunter.io/v2"

    def _make_request(self, endpoint: str, params: dict) -> dict:
        """
        Helper method to make a GET request to the Hunter API.
        
        :param endpoint: The API endpoint to call.
        :param params: The query parameters for the request.
        :return: A dictionary containing the API response.
        """
        url = f"{self.base_url}/{endpoint}"
        params['api_key'] = self.api_key

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            current_app.logger.error(f"Error making Hunter.io API call: {e}")
            return {"error": str(e)}

    def domain_search(self, domain: str) -> dict:
        """
        Search for email addresses for a given domain.
        
        :param domain: The domain to search for email addresses.
        :return: A dictionary containing the API response.
        """
        params = {"domain": domain}
        return self._make_request("domain-search", params)

    def email_finder(self, domain: str, first_name: str, last_name: str) -> dict:
        """
        Find an email address given a domain and a person's name.
        
        :param domain: The domain to search.
        :param first_name: The person's first name.
        :param last_name: The person's last name.
        :return: A dictionary containing the API response.
        """
        params = {
            "domain": domain,
            "first_name": first_name,
            "last_name": last_name
        }
        return self._make_request("email-finder", params)
