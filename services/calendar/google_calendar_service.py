from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from services.calendar.base import CalendarService


SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


class GoogleCalendarService(CalendarService):
    """Creates events in the user's primary Google Calendar."""

    def __init__(self, credentials_file: Path, token_file: Path, timezone: str = "America/Mexico_City"):
        self.credentials_file = credentials_file
        self.token_file       = token_file
        self.timezone         = timezone
        self._service         = None

    # ── Public API ────────────────────────────────────────

    def create_event(self, title: str, start: datetime, end: datetime, description: str = "") -> str:
        svc = self._get_service()

        event = {
            "summary":     title,
            "description": description,
            "start": {"dateTime": start.isoformat(), "timeZone": self.timezone},
            "end":   {"dateTime": end.isoformat(),   "timeZone": self.timezone},
        }

        result = svc.events().insert(calendarId="primary", body=event).execute()
        return result["id"]

    # ── Auth helpers ──────────────────────────────────────

    def _get_service(self):
        if self._service:
            return self._service

        creds = None
        if self.token_file.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_file), SCOPES
                )
                creds = flow.run_local_server(port=0)

            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            self.token_file.write_text(creds.to_json(), encoding="utf-8")

        self._service = build("calendar", "v3", credentials=creds)
        return self._service
