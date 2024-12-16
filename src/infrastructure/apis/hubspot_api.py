import os
import requests
from dotenv import load_dotenv

class HubSpotAPI:
    """
    HubSpotAPI class to interact with HubSpot's CRM API, providing methods to manage contacts and companies.
    
    Attributes:
        access_token (str): The API token for authenticating requests to the HubSpot API.
        headers (dict): The headers to include in API requests.
    """
    
    def __init__(self):
        # Load the access token from the .env file or Flask app config
        load_dotenv()
        self.access_token = os.getenv("HUBSPOT_ACCESS_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        self.contacts_url = "https://api.hubapi.com/crm/v3/objects/contacts"
        self.companies_url = "https://api.hubapi.com/crm/v3/objects/companies"

    def get_contacts(self, limit: int) -> dict:
        """
        Fetches all contacts from HubSpot CRM.
        
        Returns:
            dict: A dictionary containing the results of the request.
                  Includes either the contacts data or an error message.
        """
        response = requests.get(self.contacts_url, headers=self.headers)
        if response.status_code == 200:
            contacts = response.json()
            return {
                "success": True,
                "contacts": contacts['results']
            }
        else:
            return {
                "success": False,
                "error": f"Failed to fetch contacts. Status code: {response.status_code}, Response: {response.text}"
            }

    def create_contact(self, first_name: str, last_name: str, email: str) -> dict:
        """
        Creates a new contact in HubSpot CRM.
        
        Args:
            first_name (str): The first name of the contact.
            last_name (str): The last name of the contact.
            email (str): The email address of the contact.
            
        Returns:
            dict: A dictionary containing the result of the creation operation,
                  including the contact ID or an error message.
        """
        data = {
            "properties": {
                "firstname": first_name,
                "lastname": last_name,
                "email": email
            }
        }
        response = requests.post(self.contacts_url, headers=self.headers, json=data)
        if response.status_code == 201:
            contact = response.json()
            return {
                "success": True,
                "contact_id": contact['id']
            }
        else:
            return {
                "success": False,
                "error": f"Failed to create contact. Status code: {response.status_code}, Response: {response.text}"
            }

    def update_contact(self, contact_id: str, updated_data: dict) -> dict:
        """
        Updates an existing contact in HubSpot CRM by contact ID.
        
        Args:
            contact_id (str): The ID of the contact to update.
            updated_data (dict): A dictionary of the properties to update.
        
        Returns:
            dict: A dictionary containing the result of the update operation.
                  Indicates success or provides an error message.
        """
        url = f"{self.contacts_url}/{contact_id}"
        data = {"properties": updated_data}
        response = requests.patch(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Contact with ID {contact_id} updated successfully!"
            }
        else:
            return {
                "success": False,
                "error": f"Failed to update contact. Status code: {response.status_code}, Response: {response.text}"
            }

    def delete_contact(self, contact_id: str) -> dict:
        """
        Deletes a contact from HubSpot CRM by contact ID.
        
        Args:
            contact_id (str): The ID of the contact to delete.
        
        Returns:
            dict: A dictionary indicating the result of the delete operation.
        """
        url = f"{self.contacts_url}/{contact_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            return {
                "success": True,
                "message": f"Contact with ID {contact_id} deleted successfully!"
            }
        else:
            return {
                "success": False,
                "error": f"Failed to delete contact. Status code: {response.status_code}, Response: {response.text}"
            }

    def get_companies(self) -> dict:
        """
        Fetches all companies from HubSpot CRM.
        
        Returns:
            dict: A dictionary containing the results of the request,
                  includes either the companies data or an error message.
        """
        response = requests.get(self.companies_url, headers=self.headers)
        if response.status_code == 200:
            companies = response.json()
            return {
                "success": True,
                "companies": companies['results']
            }
        else:
            return {
                "success": False,
                "error": f"Failed to fetch companies. Status code: {response.status_code}, Response: {response.text}"
            }

    def create_company(self, company_name: str, domain: str) -> dict:
        """
        Creates a new company in HubSpot CRM.
        
        Args:
            company_name (str): The name of the company.
            domain (str): The domain of the company.
            
        Returns:
            dict: A dictionary containing the result of the creation operation,
                  including the company ID or an error message.
        """
        data = {
            "properties": {
                "name": company_name,
                "domain": domain
            }
        }
        response = requests.post(self.companies_url, headers=self.headers, json=data)
        if response.status_code == 201:
            company = response.json()
            return {
                "success": True,
                "company_id": company['id']
            }
        else:
            return {
                "success": False,
                "error": f"Failed to create company. Status code: {response.status_code}, Response: {response.text}"
            }

    def update_company(self, company_id: str, updated_data: dict) -> dict:
        """
        Updates an existing company in HubSpot CRM by company ID.
        
        Args:
            company_id (str): The ID of the company to update.
            updated_data (dict): A dictionary of the properties to update.
        
        Returns:
            dict: A dictionary containing the result of the update operation.
                  Indicates success or provides an error message.
        """
        url = f"{self.companies_url}/{company_id}"
        data = {"properties": updated_data}
        response = requests.patch(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Company with ID {company_id} updated successfully!"
            }
        else:
            return {
                "success": False,
                "error": f"Failed to update company. Status code: {response.status_code}, Response: {response.text}"
            }

    def delete_company(self, company_id: str) -> dict:
        """
        Deletes a company from HubSpot CRM by company ID.
        
        Args:
            company_id (str): The ID of the company to delete.
        
        Returns:
            dict: A dictionary indicating the result of the delete operation.
        """
        url = f"{self.companies_url}/{company_id}"
        response = requests.delete(url, headers=self.headers)
        if response.status_code == 204:
            return {
                "success": True,
                "message": f"Company with ID {company_id} deleted successfully!"
            }
        else:
            return {
                "success": False,
                "error": f"Failed to delete company. Status code: {response.status_code}, Response: {response.text}"
            }
