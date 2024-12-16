import os
import requests
# from dotenv import load_dotenv
from typing import Optional, Dict, Any, List

class NewsAPIInitializer:
    def __init__(self) -> None:
        """
        Initializes the NewsAPI by loading environment variables
        from the .env file and setting up the API key and base URL.
        """
        # Load environment variables from .env file
        # load_dotenv()
        
        # Configuration
        self.api_key: str = os.getenv("NEWS_API_KEY", "your_default_api_key")
        self.api_base_url: str = "https://newsapi.org/v2"

    def get_top_headlines(
        self,
        country: Optional[str] = None,
        category: Optional[str] = None,
        sources: Optional[str] = None,
        q: Optional[str] = None,
        pageSize: int = 20,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Fetches the top headlines from the News API.

        Args:
            country (Optional[str]): The country code (e.g., 'us') to filter the headlines.
            category (Optional[str]): The category of news (e.g., 'technology').
            sources (Optional[str]): Comma-separated string of sources to filter the articles.
            q (Optional[str]): A keyword or phrase to search for in the articles.
            pageSize (int): The number of articles to return per page (default is 20).
            page (int): The page number to retrieve (default is 1).

        Returns:
            Dict[str, Any]: The JSON response from the API containing headlines and articles.
        """
        endpoint = f"{self.api_base_url}/top-headlines"
        headers = {
            "X-Api-Key": self.api_key
        }
        params = {
            "country": country,
            "category": category,
            "sources": sources,
            "q": q,
            "pageSize": pageSize,
            "page": page
        }
        
        # Remove None values from params
        params = {k: v for k, v in params.items() if v is not None}
        print("pß", params)
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        print(response.json())
        return response.json()


# NewsAPI = NewsAPIInitializer()
