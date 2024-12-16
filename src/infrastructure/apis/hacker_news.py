import requests
from typing import Any, Dict, List

class HackerNewsAPI:
    """
    A class to interact with the Hacker News API to fetch stories, comments, jobs, polls, and users.
    """

    BASE_URL = "https://hacker-news.firebaseio.com/v0"

    def _make_request(self, endpoint: str) -> Dict[str, Any]:
        """
        Helper method to make a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to request.

        Returns:
            Dict[str, Any]: The response data as a JSON dictionary.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        response = requests.get(f"{self.BASE_URL}/{endpoint}.json")

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_item(self, item_id: int) -> Dict[str, Any]:
        """
        Fetch a specific item by ID (story, comment, poll, etc.).

        Args:
            item_id (int): The ID of the item to fetch.

        Returns:
            Dict[str, Any]: The details of the fetched item.
        """
        return self._make_request(f"item/{int(item_id)}")

    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch a specific user by ID.

        Args:
            user_id (str): The ID of the user to fetch.

        Returns:
            Dict[str, Any]: The details of the fetched user.
        """
        return self._make_request(f"user/{user_id}")

    def get_max_item(self) -> int:
        """
        Fetch the current largest item ID.

        Returns:
            int: The max item ID.
        """
        return self._make_request("maxitem")

    def get_top_stories(self) -> List[int]:
        """
        Fetch the top 500 stories on Hacker News.

        Returns:
            List[int]: A list of top story IDs.
        """
        return self._make_request("topstories")

    def get_new_stories(self) -> List[int]:
        """
        Fetch the newest 500 stories on Hacker News.

        Returns:
            List[int]: A list of new story IDs.
        """
        return self._make_request("newstories")

    def get_best_stories(self) -> List[int]:
        """
        Fetch the best 500 stories on Hacker News.

        Returns:
            List[int]: A list of best story IDs.
        """
        return self._make_request("beststories")

    def get_ask_stories(self) -> List[int]:
        """
        Fetch the latest 200 Ask HN stories.

        Returns:
            List[int]: A list of Ask HN story IDs.
        """
        return self._make_request("askstories")

    def get_show_stories(self) -> List[int]:
        """
        Fetch the latest 200 Show HN stories.

        Returns:
            List[int]: A list of Show HN story IDs.
        """
        return self._make_request("showstories")

    def get_job_stories(self) -> List[int]:
        """
        Fetch the latest 200 job stories.

        Returns:
            List[int]: A list of job story IDs.
        """
        return self._make_request("jobstories")
    
    def get_updates(self) -> Dict[str, Any]:
        """
        Fetch changed items and profiles.

        Returns:
            Dict[str, Any]: A dictionary containing updated item IDs and updated profile usernames.
        """
        return self._make_request("updates")
    