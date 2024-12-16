import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YelpClient:
    def __init__(self):
        self.api_key = os.getenv('YELP_API_KEY')
        if not self.api_key:
            raise ValueError("Yelp API Key is missing. Please set it in your environment variables.")
        self.base_url = "https://api.yelp.com/v3"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def _get(self, endpoint, params={}):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Successfully fetched data from {endpoint}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from {endpoint}: {e}")
            return {"error": str(e)}

    def search_businesses(self, location, term=""):
        endpoint = "businesses/search"
        params = {"location": location, "term": term}
        return self._get(endpoint, params)
    
    def get_business(self, business_id):
        endpoint = f"businesses/{business_id}"
        return self._get(endpoint)

    def get_business_reviews(self, business_id):
        endpoint = f"businesses/{business_id}/reviews"
        return self._get(endpoint)

    def list_categories(self):
        endpoint = "categories"
        return self._get(endpoint)
    
    def search_events(self, location, categories=None):
        endpoint = "events"
        params = {"location": location}
        if categories:
            params['categories'] = categories
        return self._get(endpoint, params)

    def get_event(self, event_id):
        endpoint = f"events/{event_id}"
        return self._get(endpoint)

    def search_by_transaction(self, location, transaction_type="delivery"):
        endpoint = f"transactions/{transaction_type}/search"
        params = {"location": location}
        return self._get(endpoint, params)

    def autocomplete(self, text, latitude=None, longitude=None):
        endpoint = "autocomplete"
        params = {"text": text}
        if latitude and longitude:
            params["latitude"] = latitude
            params["longitude"] = longitude
        return self._get(endpoint, params)

