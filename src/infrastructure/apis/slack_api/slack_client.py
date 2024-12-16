from datetime import datetime
import os
# from slack_sdk import WebClient
# from slack_sdk.errors import SlackApiError
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlackClient:
    def __init__(self):
        self.client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")
        self.user_client = WebClient(token=os.getenv("SLACK_USER_BOT_TOKEN"))
    
    def send_message(self, text, channel=None):
        """
        Send a message to a Slack channel.
        
        :param text: The message text to send.
        :param channel: The Slack channel ID. If None, uses the default channel.
        :return: Response from Slack API or error message.
        """
        target_channel = channel if channel else self.channel_id
        try:
            response = self.client.chat_postMessage(
                channel=target_channel,
                text=text
            )
            logger.info(f"Message sent to {target_channel}: {text}")
            return response
        except SlackApiError as e:
            error_message = f"Error sending message: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}
    
    def get_user_info(self, user_id):
        """
        Retrieve information about a Slack user.
        
        :param user_id: The Slack user ID.
        :return: User information or error message.
        """
        try:
            response = self.client.users_info(user=user_id)
            logger.info(f"Fetched user info for user_id: {user_id}")
            return response['user']
        except SlackApiError as e:
            error_message = f"Error fetching user info: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}
    
    def send_message_with_blocks(self, blocks, channel=None, text=""):
        """
        Send a message with blocks to a Slack channel.
        
        :param blocks: A list of block elements.
        :param channel: The Slack channel ID. If None, uses the default channel.
        :param text: Fallback text for notifications.
        :return: Response from Slack API or error message.
        """
        target_channel = channel if channel else self.channel_id
        try:
            response = self.client.chat_postMessage(
                channel=target_channel,
                text=text,
                blocks=blocks
            )
            logger.info(f"Block message sent to {target_channel}")
            return response
        except SlackApiError as e:
            error_message = f"Error sending block message: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}
        
    def list_conversations(self, types="public_channel,private_channel", limit=100):
        """
        List all conversations (channels) in the Slack workspace.

        :param types: Conversation types to include (e.g., 'public_channel,private_channel').
        :param limit: Maximum number of results to return.
        :return: List of channels or error message.
        """
        try:
            response = self.client.conversations_list(types=types, limit=limit)
            channels = response['channels']
            logger.info(f"Retrieved {len(channels)} channels.")
            return channels
        except SlackApiError as e:
            error_message = f"Error listing conversations: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def get_conversation_history(self, channel_id, limit=100):
        """
        Retrieve message history of a conversation (channel).

        :param channel_id: The ID of the channel.
        :param limit: Maximum number of messages to retrieve.
        :return: List of messages or error message.
        """
        try:
            response = self.client.conversations_history(channel=channel_id, limit=limit)
            messages = response['messages']
            logger.info(f"Retrieved {len(messages)} messages from channel {channel_id}.")
            return messages
        except SlackApiError as e:
            error_message = f"Error retrieving conversation history: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def join_conversation(self, channel_id):
        """
        Join a conversation (channel).

        :param channel_id: The ID of the channel to join.
        :return: Response from Slack API or error message.
        """
        try:
            response = self.client.conversations_join(channel=channel_id)
            logger.info(f"Joined channel {channel_id}.")
            return response
        except SlackApiError as e:
            error_message = f"Error joining conversation: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def create_conversation(self, name, is_private=False):
        """
        Create a new conversation (channel).

        :param name: The name of the channel to create.
        :param is_private: Whether to create a private channel.
        :return: Channel information or error message.
        """
        try:
            response = self.client.conversations_create(name=name, is_private=is_private)
            channel = response['channel']
            logger.info(f"Created channel '{name}' with ID {channel['id']}.")
            return channel
        except SlackApiError as e:
            error_message = f"Error creating conversation: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}
        
    # def add_reminder(self, text, time, recurring=False, recurrence=None):
    #     """
    #     Adds a reminder with optional recurrence.
    #     """
    #     try:
    #         print(f"Received time: {time}")

    #         parsed_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
    #         unix_time = int(parsed_time.timestamp())

    #         reminder_args = {"text": text, "time": unix_time}
    #         if recurring and recurrence:
    #             reminder_args["recurrence"] = recurrence

    #         response = self.user_client.reminders_add(**reminder_args)
    #         logger.info(f"Added reminder: {text} at {time}, Recurring: {recurring}")
    #         return response['reminder']
    #     except ValueError as ve:
    #         logger.error("ValueError in time parsing: ", ve)
    #         return {"error": "Error parsing the time. Ensure it's in 'YYYY-MM-DDTHH:MM:SS' format."}
    #     except SlackApiError as e:
    #         logger.error("Slack API error: ", e.response['error'])
    #         return {"error": f"Error adding reminder: {e.response['error']}"}
    
    def add_reminder(self, text, time, recurring=False, recurrence=None):
        """
        Adds a reminder with optional recurrence.
        """
        try:
            parsed_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            unix_time = int(parsed_time.timestamp())
    
            reminder_args = {"text": text, "time": unix_time}
            if recurring and recurrence:
                reminder_args["recurrence"] = recurrence
    
            response = self.user_client.reminders_add(**reminder_args)
            logger.info(f"Added reminder: {text} at {time}, Recurring: {recurring}")
            return response['reminder']
        except ValueError as ve:
            logger.error(f"ValueError in time parsing: {ve}")
            return {"error": "Error parsing the time. Ensure it's in 'YYYY-MM-DDTHH:MM:SS' format."}
        except SlackApiError as e:
            logger.error(f"Slack API error: {e.response['error']}")
            return {"error": f"Error adding reminder: {e.response['error']}"}


    def list_reminders(self):
        """
        Lists all reminders for the authenticated user.

        :return: List of reminders or error message.
        """
        try:
            response = self.client.reminders_list()
            reminders = response['reminders']
            logger.info("Retrieved reminders list.")
            return reminders
        except SlackApiError as e:
            error_message = f"Error listing reminders: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def complete_reminder(self, reminder_id):
        """
        Marks a reminder as complete.

        :param reminder_id: The ID of the reminder to mark complete.
        :return: Response from Slack API or error message.
        """
        try:
            response = self.client.reminders_complete(reminder=reminder_id)
            logger.info(f"Completed reminder with ID: {reminder_id}")
            return response
        except SlackApiError as e:
            error_message = f"Error completing reminder: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def delete_reminder(self, reminder_id):
        """
        Deletes a reminder.

        :param reminder_id: The ID of the reminder to delete.
        :return: Response from Slack API or error message.
        """
        try:
            response = self.client.reminders_delete(reminder=reminder_id)
            logger.info(f"Deleted reminder with ID: {reminder_id}")
            return response
        except SlackApiError as e:
            error_message = f"Error deleting reminder: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}
        
    def get_upload_url(self, filename, length):
        """
        Obtains an upload URL for a file to be uploaded to Slack.

        :param filename: The name of the file being uploaded.
        :param length: The size of the file in bytes.
        :return: Upload URL and file ID or error message.
        """
        try:
            response = self.client.files_getUploadURLExternal(filename=filename, length=length)
            logger.info(f"Obtained upload URL for file: {filename}")
            return response['upload_url'], response['file_id']
        except SlackApiError as e:
            error_message = f"Error obtaining upload URL: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def complete_upload(self, file_id, channels, title=None):
        """
        Finalizes a file upload, making it available in Slack.

        :param file_id: The ID of the uploaded file.
        :param channels: Comma-separated list of channel IDs where the file will be shared.
        :param title: Optional title for the file.
        :return: Response from Slack API or error message.
        """
        try:
            files = [{"id": file_id, "title": title}]
            response = self.client.files_completeUploadExternal(files=files, channel_id=channels)
            logger.info(f"Completed upload for file ID: {file_id}")
            return response
        except SlackApiError as e:
            error_message = f"Error completing upload: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def upload_file_to_url(self, upload_url, file_path):
        """
        Uploads the file data to the specified upload URL.

        :param upload_url: The URL to upload the file to.
        :param file_path: The local path to the file being uploaded.
        :return: Response status of the upload or error message.
        """
        try:
            with open(file_path, 'rb') as file_data:
                response = requests.post(upload_url, files={"file": file_data})
                response.raise_for_status()
            logger.info(f"Uploaded file to {upload_url}")
            return {"status": "success"}
        except requests.exceptions.RequestException as e:
            error_message = f"Error uploading file to URL: {str(e)}"
            logger.error(error_message)
            return {"error": error_message}

    def list_files(self, channel=None, count=100):
        """
        Lists files in Slack.

        :param channel: Filter files to a specific channel (optional).
        :param count: Maximum number of files to retrieve.
        :return: List of files or error message.
        """
        try:
            response = self.client.files_list(channel=channel, count=count)
            files = response['files']
            logger.info(f"Retrieved {len(files)} files.")
            return files
        except SlackApiError as e:
            error_message = f"Error listing files: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def delete_file(self, file_id):
        """
        Deletes a file from Slack.

        :param file_id: The ID of the file to delete.
        :return: Response from Slack API or error message.
        """
        try:
            response = self.client.files_delete(file=file_id)
            logger.info(f"Deleted file with ID: {file_id}")
            return response
        except SlackApiError as e:
            error_message = f"Error deleting file: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}
        
    def get_team_info(self):
        """
        Retrieves information about the Slack workspace.

        :return: Workspace information or error message.
        """
        try:
            response = self.client.team_info()
            logger.info("Retrieved workspace information.")
            return response['team']
        except SlackApiError as e:
            error_message = f"Error retrieving workspace information: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

    def get_team_profile(self):
        """
        Retrieves the profile fields for the Slack workspace.

        :return: Profile fields or error message.
        """
        try:
            response = self.client.team_profile_get()
            logger.info("Retrieved workspace profile fields.")
            return response['profile']
        except SlackApiError as e:
            error_message = f"Error retrieving workspace profile fields: {e.response['error']}"
            logger.error(error_message)
            return {"error": error_message}

