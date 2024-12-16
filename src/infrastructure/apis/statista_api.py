"""
This class provides methods to interact with the Statista API.
It includes methods to retrieve statistics, infographics, studies, and market insights.

Classes:
    StatistaAPI: A class to interact with the Statista API.

Methods:
    get_statistics: Retrieve statistics from the Statista API based on query parameters.
    get_statistics_by_id: Retrieve a specific statistic by its ID.
    get_infographics: Retrieve infographics from the Statista API based on query parameters.
    get_infographic_by_id: Retrieve a specific infographic by its ID.
    get_studies: Retrieve studies from the Statista API based on query parameters.
    get_study_by_id: Retrieve a specific study by its ID.
    get_market_insights: Retrieve market insights from the Statista API based on query parameters.

Parameters for API methods:
    id (int): The ID of the item to retrieve.
    query (str): The search query to filter by.
    limit (int): The maximum number of items to return. Default is 20.
    platform (str): The platform to retrieve items from ('de', 'en', 'fr', 'es').
    date_from (str): The earliest publication date in YYYY-MM-DD format.
    date_to (str): The latest publication date in YYYY-MM-DD format.
    premium (int): 1 for premium only, 0 for free only. Default is None (both).
    industry (int): The ID of the industry to filter by.
    geolocation (int): The ID of the geolocation to filter by.
    sort (int): Sort by relevance (0), date (1), or popularity (2).
    page (int): The pagination page number. Default is 1.

    """

from flask import request, jsonify, Blueprint
from typing import Optional, Dict, Any

import requests

# from backend.src.interfaces.infrastructure_interfaces.api_interfaces.statista_api_interface import IStatistaAPI

BASE_URL = 'https://api.statista.com/api/v2'

# enum for sort options
class SortOptions:
    RELEVANCE = 0
    DATE = 1
    POPULARITY = 2

class StatistaAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = BASE_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

    def get_statistics(self, id: Optional[int] = None, query: Optional[str] = None, limit: int = 20, platform: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None, premium: Optional[int] = None, industry: Optional[int] = None, geolocation: Optional[int] = None, sort: int = SortOptions.RELEVANCE, page: int = 1) -> Optional[Dict[str, Any]]:
        # Parameters to filter the API call
        params = {
            'id': id,                # ID of a single statistic
            'q': query,              # Search query
            'limit': limit,          # Limit of statistics to return
            'platform': platform,    # 'de', 'en', 'fr', or 'es'
            'date_from': date_from,  # Earliest publication date in YYYY-MM-DD
            'date_to': date_to,      # Latest publication date in YYYY-MM-DD
            'premium': premium,      # 1 for premium only, 0 for free only
            'industry': industry,    # Industry ID
            'geolocation': geolocation,  # Geolocation ID
            'sort': sort,            # 0 for relevance, 1 for date, 2 for popularity
            'page': page             # Pagination page number
        }

        # Remove None values to avoid passing unnecessary parameters
        params = {k: v for k, v in params.items() if v is not None}

        # Send the GET request
        url = f'{self.base_url}/statistics'
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            # Successful request
            data = response.json()
            return data
        else:
            # If the request failed, print the status and error message
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        
    def get_statistics_by_id(self, stat_id: int) -> Optional[Dict[str, Any]]:
        params = {
            'id': stat_id
        }

        url = f'{self.base_url}/statistics/{id}'
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        
    def get_infographics(self, id: Optional[int] = None, query: Optional[str] = None, limit: int = 20, platform: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None, premium: Optional[int] = None, industry: Optional[int] = None, geolocation: Optional[int] = None, sort: int = SortOptions.RELEVANCE, page: int = 1) -> Optional[Dict[str, Any]]:
        params = {
            id: id,
            'q': query,
            'limit': limit,
            'platform': platform,
            'date_from': date_from,
            'date_to': date_to,
            'premium': premium,
            'industry': industry,
            'geolocation': geolocation,
            'sort': sort,
            'page': page
        }

        params = {k: v for k, v in params.items() if v is not None}

        url = f'{self.base_url}/infographics'
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text) 
            return None

    def get_infographic_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        params = {
            'id': id    
        }

        url = f'{self.base_url}/infographics/{id}'
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None       
    
    def get_studies(self, id: Optional[int] = None, query: Optional[str] = None, limit: int = 20, platform: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None, premium: Optional[int] = None, industry: Optional[int] = None, geolocation: Optional[int] = None, sort: int = SortOptions.RELEVANCE, page: int = 1) -> Optional[Dict[str, Any]]:
        params = {
            'id': id,
            'q': query,
            'limit': limit,
            'platform': platform,
            'date_from': date_from,
            'date_to': date_to,
            'premium': premium,
            'industry': industry,
            'geolocation': geolocation,
            'sort': sort,
            'page': page
        }

        params = {k: v for k, v in params.items() if v is not None}

        url = f'{self.base_url}/studies'
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        
    def get_study_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        params = {
            'id': id    
        }

        url = f'{self.base_url}/studies/{id}'
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        
    def get_market_insights(self, id: Optional[int] = None, query: Optional[str] = None, limit: int = 20, platform: Optional[str] = None, date_from: Optional[str] = None, date_to: Optional[str] = None, geolocation: Optional[int] = None, sort: int = SortOptions.RELEVANCE, page: int = 1) -> Optional[Dict[str, Any]]:
        params = {
            'id': id,
            'q': query,
            'limit': limit,
            'platform': platform,
            'date_from': date_from,
            'date_to': date_to,
            'geolocation': geolocation,
            'sort': sort,
            'page': page
        }

        params = {k: v for k, v in params.items() if v is not None}
        
        url = f'{self.base_url}/marketinsights'
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None
        