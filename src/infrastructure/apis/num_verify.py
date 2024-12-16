import requests
import logging
import os


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NumVerifyClient:
    def __init__(self):
        self.numverify_api_key = os.getenv('NUMVERIFY_API_KEY')
        if not self.numverify_api_key:
            raise ValueError("NumVerify API Key is missing. Please set it in your environment variables.")
        
        self.numverify_url = "http://apilayer.net/api/validate"
    

    def validate_phone_number(self, phone_number):
        params = {'access_key': self.numverify_api_key, 'number': phone_number}
        return self._make_request(self.numverify_url, params)


    def validate_international_number(self, phone_number, country_code):
        params = {
            'access_key': self.numverify_api_key,
            'number': phone_number,
            'country_code': country_code
        }
        return self._make_request(self.numverify_url, params)


    def check_carrier_info(self, phone_number):
        params = {'access_key': self.numverify_api_key, 'number': phone_number}
        return self._make_request(self.numverify_url, params)

    def bulk_validate_phone_numbers(self, phone_numbers):
        results = {}
        for number in phone_numbers:
            results[number] = self.validate_phone_number(number)
        return results


    def _make_request(self, url, params=None):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from {url}: {e}")
            return {"error": str(e)}


    
