from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.core.config import settings
from datetime import datetime, timedelta

class CalendarService:
    def __init__(self, token: str):
        self.creds = Credentials(token)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def list_events(self, max_results: int = 10):
        now = datetime.utcnow().isoformat() + 'Z'
        events_result = self.service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=max_results, singleEvents=True,
                                              orderBy='startTime').execute()
        return events_result.get('items', [])

    def create_event(self, summary: str, start_time: str, end_time: str, attendees: list = []):
        event = {
            'summary': summary,
            'start': {'dateTime': start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': end_time, 'timeZone': 'UTC'},
            'attendees': [{'email': email} for email in attendees],
        }
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        return event
