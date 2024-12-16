import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PinterestClient:
    def __init__(self):
        self.access_token = os.getenv("PINTEREST_ACCESS_TOKEN")
        self.base_url = "https://api.pinterest.com/v1"
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
    
    def get_user_info(self):
        """
        Retrieves information about the authenticated user.
        """
        endpoint = f"{self.base_url}/me/"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("Retrieved user info")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching user info: {e}")
            return {"error": str(e)}
    
    def get_user_boards(self):
        """
        Fetches the authenticated user's boards.
        """
        endpoint = f"{self.base_url}/me/boards/"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("Retrieved user boards")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching user boards: {e}")
            return {"error": str(e)}

    def create_pin(self, board_id, note, link=None, image_url=None):
        """
        Creates a pin on a specific board.
        """
        endpoint = f"{self.base_url}/pins/"
        payload = {
            "board": board_id,
            "note": note,
            "link": link,
            "image_url": image_url
        }
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info(f"Created pin on board {board_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating pin: {e}")
            return {"error": str(e)}

    def get_board_pins(self, board_id):
        """
        Retrieves all pins from a specific board.
        """
        endpoint = f"{self.base_url}/boards/{board_id}/pins/"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Retrieved pins from board {board_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching pins from board {board_id}: {e}")
            return {"error": str(e)}

    def get_analytics(self):
        """
        Retrieves analytics for the user's pins.
        """
        endpoint = f"{self.base_url}/me/analytics/"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("Retrieved analytics")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching analytics: {e}")
            return {"error": str(e)}

    def upload_media(self, file_path):
        """
        Uploads a media file to Pinterest.
        """
        upload_url = f"{self.base_url}/media/upload/"
        try:
            with open(file_path, 'rb') as file:
                files = {'media': file}
                response = requests.post(upload_url, headers=self.headers, files=files)
                response.raise_for_status()
                media_id = response.json().get('media_id')
                logger.info(f"Uploaded media file '{file_path}' with media ID {media_id}")
                return media_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Error uploading media: {e}")
            return {"error": str(e)}

    def get_media_info(self, media_id):
        """
        Retrieves information about an uploaded media file.
        """
        endpoint = f"{self.base_url}/media/{media_id}/"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Retrieved media info for media ID {media_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching media info: {e}")
            return {"error": str(e)}

    def get_user_following_boards(self):
        """
        Retrieves the boards the authenticated user is following.
        """
        endpoint = f"{self.base_url}/me/following/boards/"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("Retrieved following boards")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching following boards: {e}")
            return {"error": str(e)}

    def get_user_following_users(self):
        """
        Retrieves the users the authenticated user is following.
        """
        endpoint = f"{self.base_url}/me/following/users/"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info("Retrieved following users")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching following users: {e}")
            return {"error": str(e)}

    def follow_board(self, board_id):
        """
        Follows a specific board.
        """
        endpoint = f"{self.base_url}/boards/{board_id}/follow/"
        try:
            response = requests.post(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Followed board {board_id}")
            return {"status": "Board followed"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error following board {board_id}: {e}")
            return {"error": str(e)}

    def unfollow_board(self, board_id):
        """
        Unfollows a specific board.
        """
        endpoint = f"{self.base_url}/boards/{board_id}/unfollow/"
        try:
            response = requests.post(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Unfollowed board {board_id}")
            return {"status": "Board unfollowed"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error unfollowing board {board_id}: {e}")
            return {"error": str(e)}

    def follow_user(self, user_id):
        """
        Follows a specific user.
        """
        endpoint = f"{self.base_url}/users/{user_id}/follow/"
        try:
            response = requests.post(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Followed user {user_id}")
            return {"status": "User followed"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error following user {user_id}: {e}")
            return {"error": str(e)}

    def unfollow_user(self, user_id):
        """
        Unfollows a specific user.
        """
        endpoint = f"{self.base_url}/users/{user_id}/unfollow/"
        try:
            response = requests.post(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Unfollowed user {user_id}")
            return {"status": "User unfollowed"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error unfollowing user {user_id}: {e}")
            return {"error": str(e)}

    def search_pins(self, query):
        """
        Searches for pins based on a query.
        """
        endpoint = f"{self.base_url}/pins/search/"
        params = {"query": query}
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved pins for query '{query}'")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching pins: {e}")
            return {"error": str(e)}
