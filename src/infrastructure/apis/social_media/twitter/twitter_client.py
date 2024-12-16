import requests
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TwitterClient:
    def __init__(self):
        self.bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        self.base_url = "https://api.twitter.com/2"
        self.headers = {"Authorization": f"Bearer {self.bearer_token}"}

    def search_recent_tweets(self, query, max_results=10):
        """
        Search recent tweets based on a query.
        :param query: Search query
        :param max_results: Number of results to return
        :return: JSON response with tweets or error message
        """
        endpoint = f"{self.base_url}/tweets/search/recent"
        params = {"query": query, "max_results": max_results}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved {len(response.json().get('data', []))} tweets for query '{query}'")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching tweets for query '{query}': {e}")
            return {"error": str(e)}

    def get_user_by_username(self, username):
        """
        Retrieve user details by username.
        :param username: Twitter username
        :return: JSON response with user data or error message
        """
        endpoint = f"{self.base_url}/users/by/username/{username}"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Retrieved details for user '{username}'")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving user by username '{username}': {e}")
            return {"error": str(e)}

    def get_tweet_liking_users(self, tweet_id):
        """
        Retrieve users who liked a specific tweet.
        :param tweet_id: Tweet ID
        :return: JSON response with users or error message
        """
        endpoint = f"{self.base_url}/tweets/{tweet_id}/liking_users"
        
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            logger.info(f"Retrieved liking users for tweet ID '{tweet_id}'")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving liking users for tweet ID '{tweet_id}': {e}")
            return {"error": str(e)}

    def get_trending_topics(self, woeid=1):
        """
        Retrieve trending topics for a location.
        :param woeid: Location identifier (default is 1 for Worldwide)
        :return: JSON response with trending topics or error message
        """
        endpoint = f"https://api.twitter.com/1.1/trends/place.json"
        params = {"id": woeid}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Retrieved trending topics for location ID '{woeid}'")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving trending topics for location ID '{woeid}': {e}")
            return {"error": str(e)}

    def post_tweet(self, text):
        """
        Post a tweet.
        :param text: The content of the tweet
        :return: JSON response with tweet data or error message
        """
        endpoint = f"{self.base_url}/tweets"
        payload = {"text": text}
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info(f"Posted tweet with content '{text}'")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error posting tweet: {e}")
            return {"error": str(e)}

    def upload_media(self, file_path):
        """
        Upload media to Twitter for use in tweets.
        :param file_path: Path to the media file (e.g., image, video)
        :return: Media ID or error message
        """
        upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        try:
            with open(file_path, 'rb') as file:
                files = {'media': file}
                response = requests.post(upload_url, headers=self.headers, files=files)
                response.raise_for_status()
                media_id = response.json().get('media_id_string')
                logger.info(f"Uploaded media file '{file_path}' with media ID {media_id}")
                return media_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Error uploading media file '{file_path}': {e}")
            return {"error": str(e)}

    def create_list(self, name, description="", mode="private"):
        """
        Create a new Twitter list.
        :param name: Name of the list
        :param description: Optional description of the list
        :param mode: "private" or "public"
        :return: List information or error message
        """
        endpoint = f"{self.base_url}/lists"
        payload = {
            "name": name,
            "description": description,
            "mode": mode
        }
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            list_info = response.json()
            logger.info(f"Created list '{name}' with mode '{mode}'")
            return list_info
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating list '{name}': {e}")
            return {"error": str(e)}

    def add_member_to_list(self, list_id, user_id):
        """
        Add a user to a Twitter list.
        :param list_id: ID of the list
        :param user_id: ID of the user to add
        :return: Success or error message
        """
        endpoint = f"{self.base_url}/lists/{list_id}/members"
        payload = {"user_id": user_id}
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info(f"Added user {user_id} to list {list_id}")
            return {"status": "User added to list"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error adding user {user_id} to list {list_id}: {e}")
            return {"error": str(e)}

    def get_list_members(self, list_id):
        """
        Retrieve members of a Twitter list.
        :param list_id: ID of the list
        :return: List of members or error message
        """
        endpoint = f"{self.base_url}/lists/{list_id}/members"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            members = response.json()
            logger.info(f"Retrieved members for list {list_id}")
            return members
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving members for list {list_id}: {e}")
            return {"error": str(e)}
    def upload_media(self, file_path):
        """
        Upload media to Twitter for use in tweets.
        :param file_path: Path to the media file (e.g., image, video)
        :return: Media ID or error message
        """
        upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        try:
            with open(file_path, 'rb') as file:
                files = {'media': file}
                response = requests.post(upload_url, headers=self.headers, files=files)
                response.raise_for_status()
                media_id = response.json().get('media_id_string')
                logger.info(f"Uploaded media file '{file_path}' with media ID {media_id}")
                return media_id
        except requests.exceptions.RequestException as e:
            logger.error(f"Error uploading media file '{file_path}': {e}")
            return {"error": str(e)}

    def add_media_metadata(self, media_id, alt_text):
        """
        Add metadata (e.g., alt text) to uploaded media.
        :param media_id: Media ID returned from the media upload
        :param alt_text: Alt text for accessibility
        :return: Success or error message
        """
        metadata_url = "https://upload.twitter.com/1.1/media/metadata/create.json"
        payload = {
            "media_id": media_id,
            "alt_text": {"text": alt_text}
        }
        try:
            response = requests.post(metadata_url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.info(f"Added metadata to media with ID {media_id}")
            return {"status": "Metadata added"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error adding metadata to media with ID {media_id}: {e}")
            return {"error": str(e)}

    def create_list(self, name, description="", mode="private"):
        """
        Create a new Twitter list.
        :param name: Name of the list
        :param description: Optional description of the list
        :param mode: "private" or "public"
        :return: List information or error message
        """
        endpoint = f"https://api.twitter.com/1.1/lists/create.json"
        payload = {
            "name": name,
            "description": description,
            "mode": mode
        }
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            list_info = response.json()
            logger.info(f"Created list '{name}' with mode '{mode}'")
            return list_info
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating list '{name}': {e}")
            return {"error": str(e)}

    def get_user_lists(self):
        """
        Retrieve lists owned or subscribed by the authenticated user.
        :return: List of lists or error message
        """
        endpoint = "https://api.twitter.com/1.1/lists/list.json"
        try:
            response = requests.get(endpoint, headers=self.headers)
            response.raise_for_status()
            lists = response.json()
            logger.info("Retrieved user lists")
            return lists
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving user lists: {e}")
            return {"error": str(e)}

    def get_list_members(self, list_id):
        """
        Retrieve members of a Twitter list.
        :param list_id: ID of the list
        :return: List of members or error message
        """
        endpoint = f"https://api.twitter.com/1.1/lists/members.json"
        params = {"list_id": list_id}
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            members = response.json()
            logger.info(f"Retrieved members for list {list_id}")
            return members
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving members for list {list_id}: {e}")
            return {"error": str(e)}

    def add_member_to_list(self, list_id, user_id):
        """
        Add a user to a Twitter list.
        :param list_id: ID of the list
        :param user_id: ID of the user to add
        :return: Success or error message
        """
        endpoint = f"https://api.twitter.com/1.1/lists/members/create.json"
        params = {"list_id": list_id, "user_id": user_id}
        try:
            response = requests.post(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Added user {user_id} to list {list_id}")
            return {"status": "User added to list"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error adding user {user_id} to list {list_id}: {e}")
            return {"error": str(e)}

    def remove_member_from_list(self, list_id, user_id):
        """
        Remove a user from a Twitter list.
        :param list_id: ID of the list
        :param user_id: ID of the user to remove
        :return: Success or error message
        """
        endpoint = f"https://api.twitter.com/1.1/lists/members/destroy.json"
        params = {"list_id": list_id, "user_id": user_id}
        try:
            response = requests.post(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            logger.info(f"Removed user {user_id} from list {list_id}")
            return {"status": "User removed from list"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Error removing user {user_id} from list {list_id}: {e}")
            return {"error": str(e)}

    def show_list_details(self, list_id):
        """
        Retrieve details of a Twitter list.
        :param list_id: ID of the list
        :return: List details or error message
        """
        endpoint = f"https://api.twitter.com/1.1/lists/show.json"
        params = {"list_id": list_id}
        try:
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            list_info = response.json()
            logger.info(f"Retrieved details for list {list_id}")
            return list_info
        except requests.exceptions.RequestException as e:
            logger.error(f"Error retrieving list details for {list_id}: {e}")
            return {"error": str(e)}