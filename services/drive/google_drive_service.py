import io
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


SCOPES = ["https://www.googleapis.com/auth/drive"]
MP3_MIME  = "audio/mpeg"
FOLDER_MIME = "application/vnd.google-apps.folder"


class GoogleDriveService:
    """
    Handles all Google Drive I/O:
      - List and download MP3s from an Inbox folder
      - Upload files to a destination folder (mirroring local paths)
      - Move files within Drive
    """

    def __init__(self, credentials_file: Path, token_file: Path):
        self.credentials_file = credentials_file
        self.token_file       = token_file
        self._service         = None

    # ── Auth ─────────────────────────────────────────────

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

        self._service = build("drive", "v3", credentials=creds)
        return self._service

    # ── Inbox ─────────────────────────────────────────────

    def list_mp3s(self, folder_id: str) -> list[dict]:
        """Return list of {id, name} for every MP3 in the folder."""
        svc = self._get_service()
        query = (
            f"'{folder_id}' in parents"
            f" and mimeType='{MP3_MIME}'"
            f" and trashed=false"
        )
        result = svc.files().list(q=query, fields="files(id,name)").execute()
        return result.get("files", [])

    def download_file(self, file_id: str, dest_path: Path) -> None:
        """Download a Drive file to a local path."""
        svc     = self._get_service()
        request = svc.files().get_media(fileId=file_id)
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        with open(dest_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

    # ── Upload ────────────────────────────────────────────

    def upload_file(self, local_path: Path, folder_id: str, file_name: str = "") -> str:
        """Upload a local file to a Drive folder. Returns the new file ID."""
        svc  = self._get_service()
        name = file_name or local_path.name

        # Check if file already exists in folder → update instead of duplicate
        existing_id = self._find_file_in_folder(folder_id, name)
        media       = MediaFileUpload(str(local_path), resumable=True)

        if existing_id:
            svc.files().update(fileId=existing_id, media_body=media).execute()
            return existing_id

        metadata = {"name": name, "parents": [folder_id]}
        result   = svc.files().create(body=metadata, media_body=media, fields="id").execute()
        return result["id"]

    def get_or_create_subfolder(self, parent_id: str, name: str) -> str:
        """Return the ID of a subfolder, creating it if it doesn't exist."""
        svc   = self._get_service()
        query = (
            f"'{parent_id}' in parents"
            f" and name='{name}'"
            f" and mimeType='{FOLDER_MIME}'"
            f" and trashed=false"
        )
        result = svc.files().list(q=query, fields="files(id)").execute()
        files  = result.get("files", [])
        if files:
            return files[0]["id"]

        metadata = {"name": name, "mimeType": FOLDER_MIME, "parents": [parent_id]}
        folder   = svc.files().create(body=metadata, fields="id").execute()
        return folder["id"]

    # ── Move ──────────────────────────────────────────────

    def move_file(self, file_id: str, dest_folder_id: str) -> None:
        """Move a Drive file to a different folder."""
        svc  = self._get_service()
        file = svc.files().get(fileId=file_id, fields="parents").execute()
        prev = ",".join(file.get("parents", []))
        svc.files().update(
            fileId=file_id,
            addParents=dest_folder_id,
            removeParents=prev,
            fields="id,parents",
        ).execute()

    # ── Internal ──────────────────────────────────────────

    def _find_file_in_folder(self, folder_id: str, name: str) -> str | None:
        svc    = self._get_service()
        safe   = name.replace("'", "\\'")
        query  = f"'{folder_id}' in parents and name='{safe}' and trashed=false"
        result = svc.files().list(q=query, fields="files(id)").execute()
        files  = result.get("files", [])
        return files[0]["id"] if files else None
