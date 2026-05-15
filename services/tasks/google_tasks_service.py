from datetime import date
from pathlib import Path
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from services.tasks.base import TasksService


SCOPES = ["https://www.googleapis.com/auth/tasks"]
TASKLIST_NAME = "Second Brain Agent"


class GoogleTasksService(TasksService):
    """Creates tasks in a dedicated Google Tasks list."""

    def __init__(self, credentials_file: Path, token_file: Path):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self._service = None
        self._tasklist_id: Optional[str] = None

    # ── Public API ────────────────────────────────────────

    def create_task(self, title: str, notes: str = "", due_date: Optional[date] = None) -> str:
        svc = self._get_service()
        tl  = self._get_tasklist_id()

        body: dict = {"title": title}
        if notes:
            body["notes"] = notes
        if due_date:
            body["due"] = due_date.strftime("%Y-%m-%dT00:00:00.000Z")

        result = svc.tasks().insert(tasklist=tl, body=body).execute()
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

        self._service = build("tasks", "v1", credentials=creds)
        return self._service

    def _get_tasklist_id(self) -> str:
        if self._tasklist_id:
            return self._tasklist_id

        svc   = self._get_service()
        lists = svc.tasklists().list().execute()

        for tl in lists.get("items", []):
            if tl["title"] == TASKLIST_NAME:
                self._tasklist_id = tl["id"]
                return self._tasklist_id

        # Create list if it doesn't exist
        new_list = svc.tasklists().insert(body={"title": TASKLIST_NAME}).execute()
        self._tasklist_id = new_list["id"]
        print(f"[GoogleTasksService] Created task list: '{TASKLIST_NAME}'")
        return self._tasklist_id
