import os
import requests
from flask import current_app
from dotenv import load_dotenv

class HereAPI:
    """
    HereAPI is a class for interacting with the HERE API, providing methods for geocoding, reverse geocoding,
    searching nearby places, autosuggestions, discovering places, routing, traffic flow, traffic incidents, positioning, and weather reports.

    Attributes:
        api_key (str): The API key for accessing the HERE API.
        base_url (str): The base URL for various HERE API endpoints.

    Methods:
        geocode_location(location: str) -> tuple:
            Geocodes a location name to get latitude and longitude.
        
        reverse_geocode(lat: float, lng: float) -> str:
            Reverse geocodes latitude and longitude to get an address.
        
        search_nearby(lat: float, lng: float, query: str) -> list:
            Searches for nearby places based on a query.
        
        get_autosuggest(query: str, lat: float = None, lng: float = None) -> list:
            Provides autosuggestions for places based on partial input.
        
        get_discover(lat: float, lng: float, query: str) -> list:
            Discovers places around a given location using a keyword or category.
        
        get_routes(origin_lat: float, origin_lng: float, destination_lat: float, destination_lng: float, transport_mode: str = 'car') -> list:
            Provides routes between two locations.
        
        get_weather(lat: float, lng: float) -> dict:
            Provides current weather information for a given location.

        get_traffic_flow(lat: float, lng: float) -> list:
            Provides real-time traffic flow information for a given location.

        get_traffic_incidents(bbox: str) -> list:
            Provides real-time traffic incidents within a bounding box.

        get_position() -> None:
            Placeholder for positioning services.
    """
    
    def __init__(self):
        """
        Initializes the HereAPI class by loading the API key from the environment variables.
        Raises a ValueError if the API key is not found.
        """
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv('HERE_API_KEY')
        if not self.api_key:
            raise ValueError("HERE API key not found in environment variables")
        self.base_url = "https://geocode.search.hereapi.com/v1"

    def _make_request(self, endpoint: str, params: dict, custom_base_url=None) -> dict:
        """
        Helper method to make a GET request to the HERE API.
        
        :param endpoint: The API endpoint to call.
        :param params: The query parameters for the request.
        :param custom_base_url: Optionally specify a different base URL for services like traffic or weather.
        :return: A dictionary containing the API response.
        """
        base_url = custom_base_url if custom_base_url else self.base_url
        url = f"{base_url}/{endpoint}"
        params['apiKey'] = self.api_key

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            current_app.logger.error(f"Error making HERE API call: {str(e)}")
            return {}

    def geocode_location(self, location: str) -> tuple:
        params = {'q': location}
        data = self._make_request('geocode', params)
        if 'items' in data and len(data['items']) > 0:
            position = data['items'][0]['position']
            return position['lat'], position['lng']
        return None, None

    def reverse_geocode(self, lat: float, lng: float) -> str:
        params = {'at': f'{lat},{lng}'}
        data = self._make_request('revgeocode', params)
        if 'items' in data and len(data['items']) > 0:
            return data['items'][0]['address']['label']
        return "Address not found"

    def search_nearby(self, lat: float, lng: float, query: str) -> list:
        params = {'at': f'{lat},{lng}', 'q': query, 'limit': 5}
        return self._make_request('discover', params)

    def get_autosuggest(self, query: str, lat: float = None, lng: float = None) -> list:
        params = {'q': query}
        if lat and lng:
            params['at'] = f'{lat},{lng}'
        return self._make_request('autosuggest', params)

    def get_discover(self, lat: float, lng: float, query: str) -> list:
        params = {'at': f'{lat},{lng}', 'q': query, 'limit': 5}
        return self._make_request('discover', params)

    def get_routes(self, origin_lat: float, origin_lng: float, destination_lat: float, destination_lng: float, transport_mode: str = 'car') -> list:
        params = {
            'origin': f'{origin_lat},{origin_lng}',
            'destination': f'{destination_lat},{destination_lng}',
            'transportMode': transport_mode,
            'return': 'summary'
        }
        return self._make_request('routes', params)

    def get_weather(self, lat: float, lng: float) -> dict:
        params = {'latitude': lat, 'longitude': lng, 'product': 'observation'}
        return self._make_request('weather', params, custom_base_url="https://weather.ls.hereapi.com/weather/1.0/report.json")

    def get_traffic_flow(self, lat: float, lng: float) -> list:
        """
        Provides real-time traffic flow information for a given location.
        
        :param lat: Latitude of the location.
        :param lng: Longitude of the location.
        :return: A list of traffic flow details including speed and jam factor.
        """
        params = {'prox': f'{lat},{lng},5000'}
        data = self._make_request('flow.json', params, custom_base_url="https://traffic.ls.hereapi.com/traffic/6.3")
        flows = []
        if 'RWS' in data:
            for rw in data['RWS']:
                for flow_item in rw['RW']:
                    flow_data = flow_item.get('FIS', [])[0].get('FI', [])[0].get('CF', [])[0]
                    flows.append({
                        'speed': flow_data.get('SP'),  # Speed
                        'jam_factor': flow_data.get('JF')  # Jam factor
                    })
        return flows

    def get_traffic_incidents(self, bbox: str) -> list:
        """
        Provides real-time traffic incident reports within a bounding box.
        
        :param bbox: The bounding box to search for incidents (north,south,east,west).
        :return: A list of traffic incidents with type, severity, and description.
        """
        params = {'bbox': bbox}
        data = self._make_request('incidents.json', params, custom_base_url="https://traffic.ls.hereapi.com/traffic/6.3")
        incidents = []
        if 'TRAFFICITEMS' in data and 'TRAFFICITEM' in data['TRAFFICITEMS']:
            for item in data['TRAFFICITEMS']['TRAFFICITEM']:
                incidents.append({
                    'type': item.get('TRAFFICITEMTYPEDESC', 'Unknown'),
                    'severity': item.get('TRAFFICITEMSEVERITY', 'Unknown'),
                    'description': item['TRAFFICITEMDESCRIPTION'][0]['content']
                })
        return incidents

    def get_position(self):
        """
        Placeholder method for providing positioning services using Wi-Fi, cell towers, and GPS.
        Requires specific data from device sensors (Wi-Fi, cell towers), which can't be simulated here.
        """
        print("Positioning service requires device sensor data and cannot be demonstrated in this script.")
        return None
