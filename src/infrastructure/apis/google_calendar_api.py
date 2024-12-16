from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime


# GoogleCalendarApi class definition
class GoogleCalendarApi:
    def __init__(self, credentials_path, api_name="calendar", api_version="v3"):
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/calendar"]
        )
        self.service = build(api_name, api_version, credentials=self.credentials)

    def create_event(self, calendar_id, summary, start_time, end_time, description=None, location=None):
        event = {
            "summary": summary,
            "description": description,
            "location": location,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"}
        }
        created_event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        return created_event

    def list_events(self, calendar_id, time_min=None, max_results=10):
        events_result = self.service.events().list(
            calendarId=calendar_id,
            timeMin=time_min or datetime.datetime.utcnow().isoformat() + "Z",
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        return events_result.get("items", [])

    def get_event(self, calendar_id, event_id):
        event = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        return event

    def update_event(self, calendar_id, event_id, updates):
        event = self.service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        event.update(updates)
        updated_event = self.service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()
        return updated_event

    def delete_event(self, calendar_id, event_id):
        self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return {"message": "Event deleted successfully"}


