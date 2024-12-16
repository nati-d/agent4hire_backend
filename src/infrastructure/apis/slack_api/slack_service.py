import os
from .slack_api import SlackClient
from typing import Any, Dict, Union, List

class SlackService:
    def __init__(self):
        """Initialize the SlackService with a SlackClient instance."""
        self.slack_client = SlackClient()

    def notify_team(self, message: str) -> Union[Dict[str, Any], str]:
        """
        Notify the team by sending a message to the default Slack channel.

        :param message: The message text to send.
        :return: Response from Slack API or error message.
        """
        return self.slack_client.send_message(text=message)

    def get_member_info(self, user_id: str) -> Union[Dict[str, Any], str]:
        """
        Get information about a Slack team member.

        :param user_id: The Slack user ID.
        :return: User information or error message.
        """
        return self.slack_client.get_user_info(user_id)

    def send_insight(self, insight_data: str, user_id: str) -> Union[Dict[str, Any], str]:
        """
        Send real-time market insights to a specific user via DM.

        :param insight_data: The insight text to send.
        :param user_id: The Slack user ID to send the message to.
        :return: Response from Slack API or error message.
        """
        message = f"Real-Time Insight: {insight_data}"
        return self.slack_client.send_message(text=message, channel=user_id)

    def generate_business_plan(self, industry: str, user_id: str) -> Union[Dict[str, Any], str]:
        """
        Send a business plan generation message to a specific user via DM.

        :param industry: The industry for which to generate the plan.
        :param user_id: The Slack user ID to send the message to.
        :return: Response from Slack API or error message.
        """
        message = f"Generating a business plan for the {industry} industry..."
        return self.slack_client.send_message(text=message, channel=user_id)

    def list_conversations(self, types: str = "public_channel,private_channel", limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all conversations in the workspace.

        :param types: Comma-separated list of conversation types to include.
        :param limit: Maximum number of conversations to return.
        :return: List of conversations in the workspace.
        """
        return self.slack_client.list_conversations(types=types, limit=limit)

    def get_conversation_history(self, channel_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get message history for a specific channel.

        :param channel_id: The ID of the channel to retrieve history for.
        :param limit: Maximum number of messages to return.
        :return: List of messages in the channel.
        """
        return self.slack_client.get_conversation_history(channel_id=channel_id, limit=limit)

    def join_conversation(self, channel_id: str) -> Union[Dict[str, Any], str]:
        """
        Have the bot join a specific channel.

        :param channel_id: The ID of the channel to join.
        :return: Response from Slack API or error message.
        """
        return self.slack_client.join_conversation(channel_id=channel_id)

    def create_conversation(self, name: str, is_private: bool = False) -> Union[Dict[str, Any], str]:
        """
        Create a new channel in the workspace.

        :param name: The name of the new channel.
        :param is_private: Whether the channel should be private.
        :return: Response from Slack API or error message.
        """
        return self.slack_client.create_conversation(name=name, is_private=is_private)

    def add_reminder(self, text: str, time: str) -> Union[Dict[str, Any], str]:
        """
        Add a reminder for the authenticated user.

        :param text: The reminder text.
        :param time: When to send the reminder.
        :return: Response from Slack API or error message.
        """
        return self.slack_client.add_reminder(text=text, time=time)

    def list_reminders(self) -> List[Dict[str, Any]]:
        """
        List all reminders for the authenticated user.

        :return: List of reminders for the user.
        """
        return self.slack_client.list_reminders()

    def complete_reminder(self, reminder_id: str) -> Union[Dict[str, Any], str]:
        """
        Complete a reminder by ID.

        :param reminder_id: The ID of the reminder to complete.
        :return: Response from Slack API or error message.
        """
        return self.slack_client.complete_reminder(reminder_id=reminder_id)

    def delete_reminder(self, reminder_id: str) -> Union[Dict[str, Any], str]:
        """
        Delete a reminder by ID.

        :param reminder_id: The ID of the reminder to delete.
        :return: Response from Slack API or error message.
        """
        return self.slack_client.delete_reminder(reminder_id=reminder_id)

    def upload_file(self, file_path: str, channels: str, title: str = None) -> Union[Dict[str, Any], str]:
        """
        Upload a file to specified Slack channels through the external upload process.

        :param file_path: The path to the file to upload.
        :param channels: Comma-separated list of channel IDs to upload the file to.
        :param title: Optional title for the uploaded file.
        :return: Response from Slack API or error message.
        """
        filename = os.path.basename(file_path)
        length = os.path.getsize(file_path)

        upload_url_response = self.slack_client.get_upload_url(filename=filename, length=length)
        if "error" in upload_url_response:
            return upload_url_response

        upload_url, file_id = upload_url_response

        upload_response = self.slack_client.upload_file_to_url(upload_url=upload_url, file_path=file_path)
        if "error" in upload_response:
            return upload_response

        complete_response = self.slack_client.complete_upload(file_id=file_id, channels=channels, title=title)
        return complete_response

    def list_files(self, channel: str = None, count: int = 100) -> List[Dict[str, Any]]:
        """
        List files in the workspace, optionally filtered by channel.

        :param channel: Optional channel ID to filter the files by.
        :param count: Maximum number of files to return.
        :return: List of files in the workspace.
        """
        return self.slack_client.list_files(channel=channel, count=count)

    def delete_file(self, file_id: str) -> Union[Dict[str, Any], str]:
        """
        Delete a file by its ID.

        :param file_id: The ID of the file to delete.
        :return: Response from Slack API or error message.
        """
        return self.slack_client.delete_file(file_id=file_id)

    def get_team_info(self) -> Dict[str, Any]:
        """
        Get workspace information.

        :return: Information about the workspace.
        """
        return self.slack_client.get_team_info()

    def get_team_profile(self) -> Dict[str, Any]:
        """
        Get workspace profile fields.

        :return: Profile fields of the workspace.
        """
        return self.slack_client.get_team_profile()
