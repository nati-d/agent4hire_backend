import os
from dotenv import load_dotenv
from typing import Any, Dict, List
import requests
import time
from functools import wraps
from flask import current_app


# Load environment variables from .env file
load_dotenv()

class SpotifyAPI:
    """A class to interact with the Spotify API to get data on music.

    Attributes:
        BASE_URL (str): The base URL for the Spotify API.
        client_id (str): The client ID for authenticating requests to the Spotify API.
        client_secret (str): The client secret for authenticating requests to the Spotify API.
        access_token (str): The access token for authenticating requests to the Spotify API.
        token_expires (int): The timestamp when the access token expires.
    """

    BASE_URL = "https://api.spotify.com/v1"

    def __init__(self) -> None:
        """Initializes the SpotifyAPI client with the necessary token."""
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.access_token = None
        self.token_expires = time.time()

    def get_album(self, album_id: str, market: str = "US") -> Dict[str, Any]:
        """Get an album by its Spotify ID.

        :param album_id: The Spotify ID of the album.
        :type album_id: str

        :param market: The market to get the album from.
        :type market: str

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint=f"albums/{album_id}",
            params={
                "market": market,
            },
        )

    def get_albums(self, album_ids: List[str], market: str = "US") -> Dict[str, Any]:
        """Get multiple albums by their Spotify IDs.

        :param album_ids: A list of Spotify IDs of the albums.
        :type album_ids: List[str]

        :param market: The market to get the albums from.
        :type market: str

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="albums",
            params={
                "ids": ",".join(album_ids),
                "market": market,
            },
        )

    def get_album_tracks(
        self,
        album_id: str,
        market: str = "US",
        limit: int = 10,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Get the tracks of an album by its Spotify ID.

        :param album_id: The Spotify ID of the album.
        :type album_id: str

        :param market: The market to get the album from.
        :type market: str

        :param limit: The number of tracks to return.
        :type limit: int

        :param offset: The index of the first track to return.
        :type offset: int

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint=f"albums/{album_id}/tracks",
            params={
                "market": market,
                "limit": limit,
                "offset": offset,
            },
        )

    def get_artist(self, artist_id: str) -> Dict[str, Any]:
        """Get an artist by their Spotify ID.

        :param artist_id: The Spotify ID of the artist.
        :type artist_id: str

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint=f"artists/{artist_id}",
            params={},
        )

    def get_artists(self, artist_ids: List[str]):
        """Gets multiple artists by their Spotify IDs.

        :param artist_ids: A list of Spotify IDs of the artists.
        :type artist_ids: List[str]

        :return: The response data as a JSON dictionary
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="artists",
            params={"ids": ",".join(artist_ids)},
        )

    def get_artist_albums(
        self,
        artist_id: str,
        include_groups: str = "single,appears_on",
        market: str = "US",
        limit: int = 10,
        offset: int = 0,
    ):
        """Gets the albums of an artist by their Spotify ID.

        :param artist_id: The Spotify ID of the artist.
        :type artist_id: str

        :param include_groups: A comma-separated list of keywords that will be used to filter the response.
        :type include_groups: str

        :param market: The market to get the albums from.
        :type market: str

        :param limit: The number of albums to return.
        :type limit: int

        :param offset: The index of the first album to return.
        :type offset: int

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint=f"artists/{artist_id}/albums",
            params={
                "market": market,
                "limit": limit,
                "offset": offset,
                "include_groups": include_groups,
            },
        )

    def get_artist_top_tracks(self, artist_id: str, market: str = "US"):
        """Gets the top tracks of an artist by their Spotify ID.

        :param artist_id: The Spotify ID of the artist.
        :type artist_id: str

        :param market: The market to get the top tracks from.
        :type market: str

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint=f"artists/{artist_id}/top-tracks",
            params={
                "market": market,
            },
        )

    def get_artist_related_artists(self, artist_id: str):
        """Gets Spotify catalog information about artists similar to a given artist.
            Similarity is based on analysis of the Spotify community's listening history.

        :param artist_id: The Spotify ID of the artist.
        :type artist_id: str

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            params={},
            endpoint=f"artists/{artist_id}/related-artists",
        )

    def get_tracks(
        self,
        track_ids: List[str],
        market: str = "US",
    ):
        """Get Spotify catalog information for multiple tracks based on their Spotify IDs.

        :param track_ids: A list of Spotify IDs of the tracks.
        :type track_ids: List[str]

        :param market: The market to get the tracks from.
        :type market: str

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="tracks",
            params={
                "ids": ",".join(track_ids),
                "market": market,
            },
        )

    def get_several_browse_categories(
        self,
        locale: str = "en_US",
        limit: int = 10,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Get a list of categories used to tag items in Spotify (on, for example, the Spotify
            player’s “Browse” tab).

        :param locale: The desired language for the category metadata.
        :type locale: str

        :param limit: The maximum number of categories to return.
        :type limit: int

        :param offset: The index of the first category to return.
        :type offset: int

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="browse/categories",
            params={
                "locale": locale,
                "limit": limit,
                "offset": offset,
            },
        )

    def search_for_item(
        self,
        query: str,
        type: str = "album,artist,track",
        market: str = "US",
        limit: int = 10,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Get Spotify catalog information about albums, artists, playlists,
            tracks, shows, episodes or audiobooks that match a keyword string.
            Audiobooks are only available within the US, UK, Canada, Ireland,
            New Zealand and Australia markets.


        :param query: The search query.
        :type query: str

        :param type: A comma-separated list of item types to search across.
        :type type: str

        :param market: The market to search in.
        :type market: str

        :param limit: The maximum number of items to return.
        :type limit: int

        :param offset: The index of the first item to return.
        :type offset: int

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint="search",
            params={
                "q": query,
                "type": type,
                "market": market,
                "limit": limit,
                "offset": offset,
            },
        )

    def get_track(self, track_id: str, market: str = "US"):
        """Get Spotify catalog information for a single track identified by its unique Spotify ID.

        :param track_id: The Spotify ID of the track.
        :type track_id: str

        :param market: The market to get the track from.
        :type market: str

        :return: The response data as a JSON dictionary.
        :rtype: Dict[str, Any]
        """
        return self.__make_get_request(
            endpoint=f"tracks/{track_id}",
            params={
                "market": market,
            },
        )

    def __refresh_access_token(self):
        """Refreshes the access token for the Spotify API since it expires after a certain amount of time.

        To refresh the access token, you need to make a POST request to the Spotify API:
        ```
        curl -X POST "https://accounts.spotify.com/api/token"
        -H "Content-Type: application/x-www-form-urlencoded"
        -d "grant_type=client_credentials&client_id=your-client-id&client_secret=your-client-secret"
        ```
        """

        url = "https://accounts.spotify.com/api/token"

        response = requests.post(
            url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )

        response.raise_for_status()
        data = response.json()
        self.access_token = data["access_token"]
        self.token_expires = time.time() + data["expires_in"]
        self.token_type = data["token_type"]

    def __ensure_token_is_refreshed(func):
        """Decorator to refresh access token if it expired before calling the function."""
        @wraps(func)  # type: ignore
        def wrapper(self, *args, **kwargs):
            if self.access_token is None or time.time() > self.token_expires:
                self.__refresh_access_token()
                func_call_result = func(self, *args, **kwargs) # type: ignore
                return func_call_result

        return wrapper

    @__ensure_token_is_refreshed  # type: ignore
    def __make_get_request(self, endpoint: str, params: Dict) -> Dict[str, Any]:
        """Helper method to make a GET request to the Spotify API.

        :param endpoint: The API endpoint to call.
        :type endpoint: str

        :param params: The query parameters for the request.
        :type params: Dict

        :return: A dictionary containing the API response.
        :rtype: Dict[str, Any]
        """
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = requests.get(
                url,
                params=params,
                headers={"Authorization": f"{self.token_type} {self.access_token}"},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            current_app.logger.error(f"Error making Spotify API call: {e}")
            return {"error": str(e)}


# Example Usage of the Spotify API
if __name__ == "__main__":
    # put client id and client secret here, or set them as environment variables
    os.environ["SPOTIFY_CLIENT_ID"] = "***********************************" 
    os.environ["SPOTIFY_CLIENT_SECRET"] = "***********************************"

    spotify_api = SpotifyAPI()

    # get album by id
    album = spotify_api.get_album("6akEvsycLGftJxYudPjmqK")
