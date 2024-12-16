import requests

class SendGridAPI:
    BASE_URL = "https://api.sendgrid.com/v3"
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }


    def send_email(self, from_email, to_email, subject, content):
        url = f"{self.BASE_URL}/mail/send"
        payload = {
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "subject": subject
                }
            ],
            "from": {"email": from_email},
            "content": [{"type": "text/plain", "value": content}]
        }
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

  
    def get_email_statistics(self, start_date, end_date=None):
        url = f"{self.BASE_URL}/stats"
        params = {"start_date": start_date}
        if end_date:
            params["end_date"] = end_date
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

  
    def upsert_contacts(self, contacts):
        url = f"{self.BASE_URL}/marketing/contacts"
        payload = {"contacts": contacts}
        response = requests.put(url, json=payload, headers=self.headers)
        return response.json()

  
    def list_templates(self):
        url = f"{self.BASE_URL}/templates"
        response = requests.get(url, headers=self.headers)
        return response.json()

  
    def create_template(self, name):
        url = f"{self.BASE_URL}/templates"
        payload = {"name": name}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def list_suppression_groups(self):
        url = f"{self.BASE_URL}/asm/groups"
        response = requests.get(url, headers=self.headers)
        return response.json()

   
    def enable_click_tracking(self, enable_text=True):
        url = f"{self.BASE_URL}/tracking_settings/click"
        payload = {
            "enabled": True,
            "enable_text": enable_text
        }
        response = requests.patch(url, json=payload, headers=self.headers)
        return response.json()

   
    def get_account_info(self):
        url = f"{self.BASE_URL}/user/account"
        response = requests.get(url, headers=self.headers)
        return response.json()

  
    def get_email_activity(self, query_params=None):
        url = f"{self.BASE_URL}/messages"
        response = requests.get(url, headers=self.headers, params=query_params or {})
        return response.json()

    def list_api_keys(self):
        url = f"{self.BASE_URL}/api_keys"
        response = requests.get(url, headers=self.headers)
        return response.json()
