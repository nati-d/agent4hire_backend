import requests

class TwilioAPI:
    BASE_URL = "https://api.twilio.com/2010-04-01"

    def __init__(self, account_sid, auth_token):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.auth = (account_sid, auth_token)

  
    def send_sms(self, from_phone, to_phone, body):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}/Messages.json"
        payload = {
            "From": from_phone,
            "To": to_phone,
            "Body": body
        }
        response = requests.post(url, data=payload, auth=self.auth)
        return response.json()

  
    def list_messages(self):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}/Messages.json"
        response = requests.get(url, auth=self.auth)
        return response.json()

  
    def make_call(self, from_phone, to_phone, twiml_url):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}/Calls.json"
        payload = {
            "From": from_phone,
            "To": to_phone,
            "Url": twiml_url
        }
        response = requests.post(url, data=payload, auth=self.auth)
        return response.json()

 
    def list_calls(self):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}/Calls.json"
        response = requests.get(url, auth=self.auth)
        return response.json()


    def list_phone_numbers(self):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}/IncomingPhoneNumbers.json"
        response = requests.get(url, auth=self.auth)
        return response.json()


    def purchase_phone_number(self, phone_number, area_code=None):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}/IncomingPhoneNumbers.json"
        payload = {"PhoneNumber": phone_number}
        if area_code:
            payload["AreaCode"] = area_code
        response = requests.post(url, data=payload, auth=self.auth)
        return response.json()

   
    def get_account_info(self):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}.json"
        response = requests.get(url, auth=self.auth)
        return response.json()


    def list_subaccounts(self):
        url = f"{self.BASE_URL}/Accounts.json"
        response = requests.get(url, auth=self.auth)
        return response.json()

    def create_subaccount(self, friendly_name):
        url = f"{self.BASE_URL}/Accounts.json"
        payload = {"FriendlyName": friendly_name}
        response = requests.post(url, data=payload, auth=self.auth)
        return response.json()

   
    def delete_subaccount(self, subaccount_sid):
        url = f"{self.BASE_URL}/Accounts/{subaccount_sid}.json"
        response = requests.delete(url, auth=self.auth)
        return response.status_code

   
    def list_usage_records(self):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}/Usage/Records.json"
        response = requests.get(url, auth=self.auth)
        return response.json()

  
    def fetch_usage_record(self, category):
        url = f"{self.BASE_URL}/Accounts/{self.account_sid}/Usage/Records/{category}.json"
        response = requests.get(url, auth=self.auth)
        return response.json()
