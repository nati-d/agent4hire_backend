from typing import Dict, Optional
import requests

class OpenWeatherMapAPI:
    """
    A class to interact with the OpenWeatherMap One Call API 3.0.
    """

    BASE_URL = "https://api.openweathermap.org/data/2.5"

    def __init__(self, api_key: str):
        """
        Initializes the API class with the necessary credentials.

        :param api_key: API Key for accessing the OpenWeatherMap API.
        """
        self.api_key = api_key

    def get_weather(self, lat: float, lon: float, exclude: Optional[str] = None, units: str = "metric", lang: str = "en") -> Dict:
        """
        Retrieves weather data for a given location.

        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :param exclude: Data to exclude (comma-separated, e.g., 'minutely,hourly').
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :param lang: Language of the weather description.
        :return: Weather data in JSON format.
        """

        params = self.__remove_none_values({
            "lat": lat,
            "lon": lon,
            "exclude": exclude,
            "units": units,
            "lang": lang
        })
        return self._make_request("onecall", params)

    def search_weather(self, q: str) -> Dict:
        """
        Retrieves weather data for a given location.

        http://api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=d4222f343314a9a7570737877a06a431

        :param q: City name and country code divided by comma, use ISO 3166 country codes.
        :return: Weather data in JSON format.
        """

        params = {"q": q}
        return self._make_request("weather", params)

    def get_current_weather(self, lat: float, lon: float, units: str = "metric", lang: str = "en") -> Dict:
        """
        Retrieves only the current weather data for a given location.

        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :param lang: Language of the weather description.
        :return: Current weather data in JSON format.
        """
        weather_data = self.get_weather(lat, lon, exclude="minutely,hourly,daily,alerts", units=units, lang=lang)
        return weather_data.get("current", {})
    def get_daily_forecast(self, lat: float, lon: float, units: str = "metric", lang: str = "en") -> Dict:
        """
        Retrieves the daily forecast for a given location.

        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :param lang: Language of the weather description.
        :return: Daily forecast data in JSON format.
        """
        weather_data = self.get_weather(lat, lon, exclude="current,minutely,hourly,alerts", units=units, lang=lang)
        return weather_data.get("daily", [])

    def get_hourly_forecast(self, lat: float, lon: float, units: str = "metric", lang: str = "en") -> Dict:
        """
        Retrieves the hourly forecast for a given location.

        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :param lang: Language of the weather description.
        :return: Hourly forecast data in JSON format.
        """
        weather_data = self.get_weather(lat, lon, exclude="current,minutely,daily,alerts", units=units, lang=lang)
        return weather_data.get("hourly", [])

    def get_alerts(self, lat: float, lon: float, units: str = "metric", lang: str = "en") -> Dict:
        """
        Retrieves weather alerts for a given location.

        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :param lang: Language of the weather description.
        :return: Alerts data in JSON format.
        """
        weather_data = self.get_weather(lat, lon, exclude="current,minutely,hourly,daily", units=units, lang=lang)
        return weather_data.get("alerts", [])
        # url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=London&cnt=10&mode=json&units=metric"

    def get_forcast( self, q: str, cnt: int = 10, mode: str = "json", units: str = "metric") -> Dict:
        """
        Retrieves the daily forecast for a given location.

        :param q: City name and country code divided by comma, use ISO 3166 country codes.
        :param cnt: Number of days to forecast.
        :param mode: Response format ('json' or 'xml').
        :param units: Units of measurement ('metric', 'imperial', or 'standard').
        :return: Daily forecast data in JSON format.
        """
        params = {
            "q": q,
            "cnt": cnt,
            "mode": mode,
            "units": units
        }
        return self._make_request("forecast/daily", params)

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """
        Internal method to send a request to the API and handle the response.

        :param params: Dictionary of query parameters for the API call.
        :return: Response data in JSON format.
        :raises: HTTPError if the API request fails.
        """
        params['appid'] = self.api_key
        response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def __remove_none_values(self, dictionary: Dict) -> Dict:
        """
        Removes keys with None values from a dictionary.

        :param dictionary: The input dictionary.
        :return: A new dictionary with None values removed.
        """
        return {k: v for k, v in dictionary.items() if v is not None}


if __name__ == "__main__":
    api_key = "d4222f343314a9a7570737877a06a431"
    api = OpenWeatherMapAPI(api_key=api_key)
    # weather = api.get_weather(lat=40.7128, lon=-74.0060)
    # weather = api.search_weather(q="Addis Ababa")
    """
    {
        'coord': {
            'lon': 38.7469, 'lat': 9.025
        },
        'weather': [
            {'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}
        ],
        'base': 'stations',
        'main': {
            'temp': 285.55,
            'feels_like': 285.14,
            'temp_min': 285.55,
            'temp_max': 285.55,
            'pressure': 1019,
            'humidity': 88,
            'sea_level': 1019,
            'grnd_level': 770
        },
        'visibility': 10000,
        'wind': { 'speed': 0.59, 'deg': 94, 'gust': 0.91 },
        clouds': { 'all': 80 },
        'dt': 1732334187,
        'sys': { 'country': 'ET', 'sunrise': 1732332097, 'sunset': 1732374102 },
        'timezone': 10800,
        'id': 344979,
        'name': 'Addis Ababa',
        'cod': 200
    }
    """

    # print(weather)

    # weather = api.get_current_weather(lat=9.025, lon=38.7469,)
    # print(weather)

    weather = api.get_forcast("Addis Ababa")
    print(weather)
