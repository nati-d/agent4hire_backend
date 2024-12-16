from enum import Enum
import requests
from flask import current_app, json
from typing import Any, Dict, List, Optional


class CrunchbaseAPI:
    base_url = "https://api.crunchbase.com/v4/data/"

    def __init__(self):
        self.api_key = current_app.config.get('CRUNCHBASE_API_KEY')
        if not self.api_key:
            raise ValueError("Crunchbase API key not found in the Flask app configuration")

    class LocationType(Enum):
        CITY = "city"
        REGION = "region"
        COUNTRY = "country"
        CONTINENT = "continent"
        GROUP = "group"

    def search_locations(
        self,
        field_ids: List[str],
        limit: Optional[int] = 100,
        after_id: Optional[str] = None,
        before_id: Optional[str] = None,
        order: Optional[List[Dict[str, Any]]] = None,
        query: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Search for locations based on provided query parameters.
        """
        current_app.logger.debug("Search locations called with:", {
            "field_ids": field_ids,
            "limit": limit,
            "after_id": after_id,
            "before_id": before_id,
            "order": order,
            "query": query
        })

        url = f"{self.base_url}searches/locations"

        # Construct the payload
        payload = {
            "field_ids": field_ids,
            "limit": limit,
            "order": order if order else [],
            "query": query if query else []
        }

        if after_id:
            payload["after_id"] = after_id
        if before_id:
            payload["before_id"] = before_id

        headers = {
            "Content-Type": "application/json",
            "X-Cb-User-Key": self.api_key
        }

        # Make the POST request to the Crunchbase API
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.json()
        else:
            current_app.logger.error("Failed to retrieve data: %s", response.status_code)
            current_app.logger.error("Response: %s", response.text)
            return {
                "error": response.status_code,
                "message": response.text
            }

    def search_organizations(
        self,
        location_type: Optional[LocationType] = None,
        location_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Search for organizations based on location and name criteria.
        """
        current_app.logger.debug("called_with", location_name, location_type)
        print("api_key", self.api_key)
        url = f"{self.base_url}searches/organizations"

        query = []

        # Construct the payload
        payload = {
            "field_ids": [
                "identifier",
                "name",
                "location_identifiers",
                "website_url",
                "image_id",
                "image_url",
                "linkedin"
            ],
            "query": query,
            "limit": 5,
            "order": [
                {
                    "field_id": "identifier",
                    "sort": "desc"
                }
            ]
        }

        headers = {
            "Content-Type": "application/json",
            "X-Cb-User-Key": self.api_key
        }

        # Make the POST request to the Crunchbase API
        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            # process to get only the three properties
            response = response.json()
            print(response)
            result = []
            for entity in response['entities']:
                props = entity["properties"]
                result.append({
                    "name": props["name"],
                    "image_url": props["image_url"],
                    "website_url": props["website_url"]
                })

            return result
        else:
            print("Failed to retrieve data:", response.status_code)
            print("Response:", response.text)
            return response.text
