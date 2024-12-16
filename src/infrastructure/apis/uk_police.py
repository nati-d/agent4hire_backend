import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UKPoliceClient:
    def __init__(self):
        self.base_url = "https://data.police.uk/api"
        self.headers = {"Content-Type": "application/json"}

    def _get(self, endpoint, params={}):
        """
        Internal function to make GET requests to the UK Police API.
        """
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Successfully fetched data from {endpoint}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from {endpoint}: {e}")
            return {"error": str(e)}

   
    def get_crimes_at_location(self, lat, lng, date=None):
        """
        Retrieve crimes for a specific location.
        :param lat: Latitude of the location
        :param lng: Longitude of the location
        :param date: Optional date (YYYY-MM)
        :return: JSON response with crimes data
        """
        params = {'lat': lat, 'lng': lng}
        if date:
            params['date'] = date
        return self._get("crimes-at-location", params)
    
    def get_crimes_street(self, lat, lng, date=None):
        """
        Retrieve crimes on a specific street.
        :param lat: Latitude of the location
        :param lng: Longitude of the location
        :param date: Optional date (YYYY-MM)
        :return: JSON response with street crimes data
        """
        params = {'lat': lat, 'lng': lng}
        if date:
            params['date'] = date
        return self._get("crimes-street", params)

    def get_outcomes_at_location(self, lat, lng, date=None):
        """
        Retrieve crime outcomes at a specific location.
        :param lat: Latitude of the location
        :param lng: Longitude of the location
        :param date: Optional date (YYYY-MM)
        :return: JSON response with crime outcomes data
        """
        params = {'lat': lat, 'lng': lng}
        if date:
            params['date'] = date
        return self._get("outcomes-at-location", params)

    def get_outcomes_for_crime(self, crime_id):
        """
        Retrieve details of outcomes for a specific crime.
        :param crime_id: Crime ID
        :return: JSON response with crime outcomes data
        """
        return self._get(f"outcomes-crime/{crime_id}")

    def get_crimes_no_location(self, category, force, date=None):
        """
        Retrieve crimes that are not associated with any specific location.
        :param category: Crime category
        :param force: Police force
        :param date: Optional date (YYYY-MM)
        :return: JSON response with crimes data
        """
        params = {'category': category, 'force': force}
        if date:
            params['date'] = date
        return self._get("crimes-no-location", params)

    
    def get_stop_and_search_street(self, lat, lng, date=None):
        """
        Retrieve stop and search data for a specific street.
        :param lat: Latitude of the location
        :param lng: Longitude of the location
        :param date: Optional date (YYYY-MM)
        :return: JSON response with stop and search data
        """
        params = {'lat': lat, 'lng': lng}
        if date:
            params['date'] = date
        return self._get("stops-street", params)

    def get_stop_and_search_location(self, lat, lng, date=None):
        """
        Retrieve stop and search data for a specific location.
        :param lat: Latitude of the location
        :param lng: Longitude of the location
        :param date: Optional date (YYYY-MM)
        :return: JSON response with stop and search data
        """
        params = {'lat': lat, 'lng': lng}
        if date:
            params['date'] = date
        return self._get("stops-at-location", params)

    def get_stop_and_search_force(self, force, date=None):
        """
        Retrieve stop and search data for a specific police force.
        :param force: Police force ID
        :param date: Optional date (YYYY-MM)
        :return: JSON response with stop and search data
        """
        params = {'force': force}
        if date:
            params['date'] = date
        return self._get("stops-force", params)

    def get_stop_and_search_no_location(self, force, date=None):
        """
        Retrieve stop and search records that are not associated with a location.
        :param force: Police force ID
        :param date: Optional date (YYYY-MM)
        :return: JSON response with stop and search data
        """
        params = {'force': force}
        if date:
            params['date'] = date
        return self._get("stops-no-location", params)

    def get_forces(self):
        """
        Retrieve a list of all police forces available via the API.
        :return: JSON response with a list of police forces
        """
        return self._get("forces")

    def get_force_details(self, force_id):
        """
        Get detailed information about a specific police force.
        :param force_id: ID of the police force
        :return: JSON response with police force details
        """
        return self._get(f"forces/{force_id}")

    def get_neighbourhoods(self, force_id):
        """
        Retrieve a list of neighbourhoods for a specific police force.
        :param force_id: ID of the police force
        :return: JSON response with neighbourhood data
        """
        return self._get(f"forces/{force_id}/neighbourhoods")

    def get_neighbourhood_details(self, force_id, neighbourhood_id):
        """
        Get details about a specific neighbourhood.
        :param force_id: ID of the police force
        :param neighbourhood_id: ID of the neighbourhood
        :return: JSON response with neighbourhood details
        """
        return self._get(f"forces/{force_id}/neighbourhoods/{neighbourhood_id}")

    def get_neighbourhood_boundary(self, force_id, neighbourhood_id):
        """
        Get the boundary information of a specific neighbourhood.
        :param force_id: ID of the police force
        :param neighbourhood_id: ID of the neighbourhood
        :return: JSON response with neighbourhood boundary data
        """
        return self._get(f"neighbourhoods/{neighbourhood_id}/boundary")

    def get_people_in_force(self, force_id):
        """
        Retrieve a list of people (e.g., officers) associated with a specific police force.
        :param force_id: ID of the police force
        :return: JSON response with people data
        """
        return self._get(f"forces/{force_id}/people")

    def get_events(self):
        """
        Retrieve information about specific police events or operations.
        :return: JSON response with police events data
        """
        return self._get("events")


