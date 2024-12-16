from enum import Enum
from typing import Dict, Optional, Any
import requests
import os  # Import os module to access environment variables

class OrderByEnum(Enum):
    NEWEST = "newest"
    OLDEST = "oldest"
    RELEVANCE = "relevance"

class UseDateEnum(Enum):
    PUBLISHED = "published"
    FIRST_PUBLICATION = "first-publication"
    NEWSPAPER_EDITION = "newspaper-edition"
    LAST_MODIFIED = "last-modified"


class GuardianNewsAPI:
    BASE_URL = "https://content.guardianapis.com/"

    def __init__(self):
        """
        Initialize the GuardianNewsAPI with the given API key.

        Args:
            api_key (str): The API key for accessing the Guardian API.
        """
        self.api_key = os.getenv("GUARDIAN_API_KEY")  # Get API key from environment variable

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the Guardian API.

        Args:
            endpoint (str): The API endpoint to request.
            params (Optional[Dict[str, Any]]): Optional parameters for the request.

        Returns:
            Dict[str, Any]: The JSON response from the API.
        """
        if params is None:
            params = {}
        params['api-key'] = self.api_key
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(f"{self.BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_sections(self, q: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve the list of sections from the Guardian API.

        Args:
            q (Optional[str]): Return section based on the query term specified.

        Returns:
            Dict[str, Any]: The JSON response containing the list of sections.
        """
        endpoint = "sections"
        params = {
            "q": q
        }
        return self._get(endpoint, params)

    def search_articles(
        self,
        query: str,
        page: int = 1,
        page_size: int = 10,
        order_by: OrderByEnum = OrderByEnum.NEWEST,
        use_date: UseDateEnum = UseDateEnum.PUBLISHED
    ) -> Dict[str, Any]:
        """
        Search for articles on the Guardian API.

        Args:
            query (str): The search query.
            page (int): The page number to retrieve. Default is 1.
            page_size (int): The number of results per page. Default is 10.
            order_by (OrderByEnum): The order in which to sort results. Default is OrderByEnum.NEWEST.

        Returns:
            Dict[str, Any]: The JSON response containing the search results.
        """
        endpoint = "search"
        params = {
            "q": query,
            "page": page,
            "page-size": page_size,
            "order-by": order_by.value,
            "use-date": use_date.value
        }
        return self._get(endpoint, params)

    def get_article(self, article_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific article by its ID from the Guardian API.

        Args:
            article_id (str): The ID of the article to retrieve.

        Returns:
            Dict[str, Any]: The JSON response containing the article details.
        """
        endpoint = f"{article_id}"
        return self._get(endpoint)

    def get_latest_headlines(
        self,
        section: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """
        Retrieve the latest headlines from the Guardian API.

        Args:
            section (Optional[str]): The section to filter results by. Default is None.
            page (int): The page number to retrieve. Default is 1.
            page_size (int): The number of results per page. Default is 10.

        Returns:
            Dict[str, Any]: The JSON response containing the latest headlines.
        """
        endpoint = "search"
        params = {
            "order-by": OrderByEnum.NEWEST.value,
            "page": page,
            "page-size": page_size
        }
        if section:
            params["section"] = section
        return self._get(endpoint, params)

    def get_tags(self, q: Optional[str] = None) -> Dict[str, Any]:
        """
        Retrieve the list of tags from the Guardian API based on a query.

        Args:
            q (Optional[str]): Request tags containing exactly this free text.

        Returns:
            Dict[str, Any]: The JSON response containing the list of tags.
        """
        endpoint = "tags"

        params = {
            "q": q
        }
        
        return self._get(endpoint, params)
