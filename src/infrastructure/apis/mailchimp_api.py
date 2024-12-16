import os
import requests

class MailChimpApi:
    def __init__(self, server_prefix: str):
    
        self.api_key = os.getenv("MAIL_CHIMP")
        if not self.api_key:
            raise ValueError("MAIL_CHIMP environment variable is not set.")
        
        self.base_url = f"https://{server_prefix}.api.mailchimp.com/3.0"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def get_audiences(self):
        """
        Retrieve a list of audiences (lists) from MailChimp.
        :return: JSON response with audience data.
        """
        url = f"{self.base_url}/lists"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_list_members(self, list_id: str):
        """
        Retrieve members of a specific list.
        :param list_id: The unique ID of the MailChimp list.
        :return: JSON response with list member data.
        """
        url = f"{self.base_url}/lists/{list_id}/members"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def add_member_to_list(self, list_id: str, email: str, status: str = "subscribed", merge_fields: dict = None):
        """
        Add a member to a specific list.
        :param list_id: The unique ID of the MailChimp list.
        :param email: The email address of the member.
        :param status: Subscription status ("subscribed", "unsubscribed", "pending", "cleaned").
        :param merge_fields: Additional fields to merge (e.g., first name, last name).
        :return: JSON response with the new member data.
        """
        url = f"{self.base_url}/lists/{list_id}/members"
        payload = {
            "email_address": email,
            "status": status,
            "merge_fields": merge_fields or {},
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def create_campaign(self, list_id: str, subject: str, from_name: str, reply_to: str):
        """
        Create a new MailChimp campaign.
        :param list_id: The unique ID of the MailChimp list.
        :param subject: The subject of the email campaign.
        :param from_name: The name to display in the "from" field.
        :param reply_to: The email address for replies.
        :return: JSON response with the campaign data.
        """
        url = f"{self.base_url}/campaigns"
        payload = {
            "type": "regular",
            "recipients": {"list_id": list_id},
            "settings": {
                "subject_line": subject,
                "from_name": from_name,
                "reply_to": reply_to,
            },
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def send_campaign(self, campaign_id: str):
        """
        Send a campaign.
        :param campaign_id: The unique ID of the MailChimp campaign.
        :return: JSON response indicating success or failure.
        """
        url = f"{self.base_url}/campaigns/{campaign_id}/actions/send"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_campaigns(self):
        """
        Retrieve a list of campaigns.
        :return: JSON response with campaign data.
        """
        url = f"{self.base_url}/campaigns"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_templates(self):
        """
        Retrieve a list of templates.
        :return: JSON response with template data.
        """
        url = f"{self.base_url}/templates"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_template(self, name: str, html: str):
        """
        Create a new template.
        :param name: Name of the template.
        :param html: HTML content of the template.
        :return: JSON response with the created template data.
        """
        url = f"{self.base_url}/templates"
        payload = {
            "name": name,
            "html": html,
        }
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def get_reports(self):
        """
        Retrieve reports of campaigns.
        :return: JSON response with report data.
        """
        url = f"{self.base_url}/reports"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_automation_emails(self):
        """
        Retrieve a list of automation emails.
        :return: JSON response with automation email data.
        """
        url = f"{self.base_url}/automations"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def start_automation_email(self, workflow_id: str):
        """
        Start an automation email.
        :param workflow_id: The unique ID of the automation workflow.
        :return: JSON response indicating success or failure.
        """
        url = f"{self.base_url}/automations/{workflow_id}/actions/start"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


