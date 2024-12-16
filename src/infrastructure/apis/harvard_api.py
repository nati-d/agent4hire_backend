from typing import Any, Dict, Final, Optional
import requests

class HarvardAPI:
    """
    A class to interact with Harvard's LibraryCloud v2 Items API.
    """

    BASE_URL: Final[str] = "https://api.lib.harvard.edu/v2/items"

    def search_items(
        self,
        query: str,
        filter: Optional[str] = None,
        facets: Optional[str] = None,
        start: Optional[int] = 0,
        limit: Optional[int] = 10,
    ) -> Dict:
        """
        Search for items in LibraryCloud.

        :param query: Search query.
        :param filter: Optional field filtering.
        :param facets: Optional facets.
        :param start: Pagination start.
        :param limit: Pagination limit.
        :return: Search results.
        """
        params = {"q": query, "filter": filter, "facets": facets, "start": start, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        return self.__make_get_request("", params)

    def get_item(self, item_id: str) -> Dict:
        """
        Retrieve a single item by its ID.

        :param item_id: The unique identifier of the item.
        :return: Item details.
        """
        return self.__make_get_request(f"/{item_id}")

    def get_facets(self, query: str) -> Dict:
        """
        Retrieve facets for a search query.

        :param query: Search query.
        :return: Facets information.
        """
        params = {"q": query}
        return self.__make_get_request("/facets", params)

    def __make_get_request(self, endpoint: str, params: Dict[str, Any] = {}) -> Dict:
        """
        Helper function to make a GET request to the API.

        :param endpoint: API endpoint to call.
        :param params: Query parameters.
        :return: Response data as a JSON dictionary.
        """
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}


if __name__ == "__main__":
    api = HarvardAPI()

    # Search for items
    results = api.search_items(query="philosophy")
    print(results)

    # Get details of a specific item
    item = api.get_item("123456")
    print(item)

    # Retrieve facets for a query
    facets = api.get_facets(query="science")
    print(facets)
