import requests
from typing import Any, Dict, List, Union

class HealthCareAPI:
    """
    A class to interact with the HealthCare.gov API to fetch content objects,
    collections, and the content index.
    """

    BASE_URL = "https://www.healthcare.gov/api/"

    def get_content_object(self, post_title: str) -> Dict[str, Any]:
        """
        Fetch a single content object by post title.

        Args:
            post_title (str): The title of the post (slug) to fetch.

        Returns:
            Dict[str, Any]: The content object as a JSON dictionary.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"https://www.healthcare.gov/{post_title}.json"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_content_collection(self, content_type: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch a collection of content objects by type.

        Args:
            content_type (str): The type of content to fetch (e.g., 'articles', 'glossary').

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary containing a list of content objects.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.BASE_URL}{content_type}.json"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_content_index(self) -> List[Dict[str, Any]]:
        """
        Fetch the content index.

        Returns:
            List[Dict[str, Any]]: A list of summary objects for the metadata of each post.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        url = f"{self.BASE_URL}index.json"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()