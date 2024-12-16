import os
import requests
from typing import Dict, List, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CalendlyApi:
    """
    A client for interacting with the Calendly API.
    This class provides methods to access various Calendly endpoints for managing
    event types, scheduling, user information, and webhooks.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the Calendly API client.
        
        Args:
            api_key (str, optional): Your Calendly API authentication token.
                                   If not provided, will try to get from CALENDLY_API_KEY
                                   environment variable.
        
        Raises:
            ValueError: If no API key is found and CALENDLY_API_KEY environment
                      variable is not set
        """
        self.api_key = api_key or os.getenv('CALENDLY_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Calendly API key not found. Please provide it as an argument "
                "or set the CALENDLY_API_KEY environment variable."
            )
        
        self.base_url = "https://api.calendly.com"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, data: Dict = None, params: Dict = None) -> Dict:
        """
        Make an HTTP request to the Calendly API.
        
        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE)
            endpoint (str): API endpoint path
            data (Dict, optional): Request payload for POST/PUT requests
            params (Dict, optional): Query parameters for GET requests
            
        Returns:
            Dict: JSON response from the API
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.request(method, url, headers=self.headers, json=data, params=params)
        response.raise_for_status()
        return response.json()

    # Event Types endpoints
    def list_event_types(self, active: bool = None, organization: str = None) -> List[Dict]:
        """
        Retrieve a list of all event types for the authenticated user.
        
        Args:
            active (bool, optional): Filter by active status
            organization (str, optional): Filter by organization UUID
            
        Returns:
            List[Dict]: List of event type objects containing details like
                       name, duration, description, and scheduling URL
        """
        params = {}
        if active is not None:
            params['active'] = str(active).lower()
        if organization:
            params['organization'] = organization
        return self._make_request("GET", "/event_types", params=params)

    def get_event_type(self, uuid: str) -> Dict:
        """
        Get detailed information about a specific event type.
        
        Args:
            uuid (str): Unique identifier of the event type
            
        Returns:
            Dict: Detailed event type information including settings and availability
        """
        return self._make_request("GET", f"/event_types/{uuid}")

    # Scheduling endpoints
    def create_scheduling_link(self, event_type_uuid: str, email: str, name: str = None) -> Dict:
        """
        Generate a new scheduling link for an event type.
        
        Args:
            event_type_uuid (str): UUID of the event type to create a link for
            email (str): Email address of the invitee
            name (str, optional): Name of the invitee
            
        Returns:
            Dict: Details of the created scheduling link including URL
        """
        data = {
            "event_type_uuid": event_type_uuid,
            "email": email
        }
        if name:
            data["name"] = name
        return self._make_request("POST", "/scheduling_links", data)

    def list_scheduled_events(self, min_start_time: Optional[datetime] = None, 
                            max_start_time: Optional[datetime] = None,
                            status: str = None,
                            organization: str = None) -> List[Dict]:
        """
        Retrieve a list of scheduled events within an optional time range.
        
        Args:
            min_start_time (datetime, optional): Filter events starting after this time
            max_start_time (datetime, optional): Filter events starting before this time
            status (str, optional): Filter by status (active, canceled)
            organization (str, optional): Filter by organization UUID
            
        Returns:
            List[Dict]: List of scheduled event objects
        """
        params = {}
        if min_start_time:
            params["min_start_time"] = min_start_time.isoformat()
        if max_start_time:
            params["max_start_time"] = max_start_time.isoformat()
        if status:
            params["status"] = status
        if organization:
            params["organization"] = organization
        return self._make_request("GET", "/scheduled_events", params=params)

    def get_scheduled_event(self, uuid: str) -> Dict:
        """Get detailed information about a specific scheduled event."""
        return self._make_request("GET", f"/scheduled_events/{uuid}")

    def cancel_scheduled_event(self, uuid: str, reason: str = None) -> None:
        """
        Cancel a scheduled event.
        
        Args:
            uuid (str): UUID of the scheduled event
            reason (str, optional): Reason for cancellation
        """
        data = {"reason": reason} if reason else None
        return self._make_request("POST", f"/scheduled_events/{uuid}/cancellation", data)

    # Invitee endpoints
    def get_invitee(self, uuid: str) -> Dict:
        """Get information about a specific invitee."""
        return self._make_request("GET", f"/invitees/{uuid}")

    def list_invitee_no_shows(self, organization: str) -> List[Dict]:
        """List invitees who didn't show up to scheduled events."""
        return self._make_request("GET", f"/organizations/{organization}/invitee_no_shows")

    # User endpoints
    def get_current_user(self) -> Dict:
        """Get authenticated user details."""
        return self._make_request("GET", "/users/me")

    def get_user_availability(self) -> Dict:
        """Get user's availability schedules."""
        return self._make_request("GET", "/user/availability_schedules")

    def get_user_busy_times(self, user_uuid: str, start_time: datetime, 
                           end_time: datetime) -> List[Dict]:
        """
        Get a user's busy times within a date range.
        
        Args:
            user_uuid (str): UUID of the user
            start_time (datetime): Start of the range
            end_time (datetime): End of the range
        """
        params = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
        return self._make_request("GET", f"/users/{user_uuid}/busy_times", params=params)

    # Organization endpoints
    def get_organization(self, uuid: str) -> Dict:
        """Get organization details."""
        return self._make_request("GET", f"/organizations/{uuid}")

    def list_organization_memberships(self, organization: str) -> List[Dict]:
        """List all memberships for an organization."""
        return self._make_request("GET", f"/organizations/{organization}/memberships")

    def list_organization_invitations(self, org_uuid: str) -> List[Dict]:
        """List organization invitations."""
        return self._make_request("GET", f"/organizations/{org_uuid}/invitations")

    # Webhook endpoints
    def create_webhook(self, url: str, events: List[str], 
                      organization_uuid: str, signing_key: str = None) -> Dict:
        """
        Create a webhook subscription.
        
        Args:
            url (str): Webhook endpoint URL
            events (List[str]): Event types to subscribe to
            organization_uuid (str): Organization UUID
            signing_key (str, optional): Key for webhook signature verification
        """
        data = {
            "url": url,
            "events": events,
            "organization": organization_uuid,
            "scope": "organization"
        }
        if signing_key:
            data["signing_key"] = signing_key
        return self._make_request("POST", "/webhook_subscriptions", data)

    def list_webhooks(self, organization: str = None, scope: str = None) -> List[Dict]:
        """
        List webhook subscriptions.
        
        Args:
            organization (str, optional): Filter by organization UUID
            scope (str, optional): Filter by scope (user, organization)
        """
        params = {}
        if organization:
            params["organization"] = organization
        if scope:
            params["scope"] = scope
        return self._make_request("GET", "/webhook_subscriptions", params=params)

    def delete_webhook(self, uuid: str) -> None:
        """Delete a webhook subscription."""
        return self._make_request("DELETE", f"/webhook_subscriptions/{uuid}")

    def get_webhook(self, uuid: str) -> Dict:
        """Get details of a specific webhook subscription."""
        return self._make_request("GET", f"/webhook_subscriptions/{uuid}")
