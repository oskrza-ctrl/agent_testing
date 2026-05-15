from pathlib import Path

from services.drive.google_drive_service import GoogleDriveService


class DriveAgent:
    """
    Handles all Google Drive sync for the pipeline:
      - download_inbox()  : pulls MP3s from Drive Inbox → local input/
      - upload_kb_file()  : pushes a local KB file → Drive Knowledge_Base/
      - move_to_processed(): moves the original MP3 in Drive → Drive Processed/
    """

    def __init__(
        self,
        drive_svc: GoogleDriveService,
        inbox_folder_id: str,
        processed_folder_id: str,
        kb_folder_id: str,
        local_input_dir: Path,
        local_kb_dir: Path,
    ):
        self.drive_svc           = drive_svc
        self.inbox_id            = inbox_folder_id
        self.processed_id        = processed_folder_id
        self.kb_folder_id        = kb_folder_id
        self.local_input_dir     = local_input_dir
        self.local_kb_dir        = local_kb_dir

        # Maps Drive file name → Drive file ID for files downloaded this session
        self._downloaded: dict[str, str] = {}

    # ── Download phase ────────────────────────────────────

    def download_inbox(self) -> list[Path]:
        """
        List all MP3s in Drive Inbox, download new ones to local input/.
        Returns list of local paths ready for processing.
        """
        files = self.drive_svc.list_mp3s(self.inbox_id)

        if not files:
            print("[DriveAgent] No MP3s found in Drive Inbox.")
            return []

        print(f"[DriveAgent] Found {len(files)} MP3(s) in Drive Inbox.")
        local_paths = []

        for f in files:
            local_path = self.local_input_dir / f["name"]
            if local_path.exists():
                print(f"[DriveAgent] Already local, skipping download: {f['name']}")
            else:
                print(f"[DriveAgent] Downloading: {f['name']}")
                self.drive_svc.download_file(f["id"], local_path)

            self._downloaded[f["name"]] = f["id"]
            local_paths.append(local_path)

        return local_paths

    # ── Upload phase ──────────────────────────────────────

    def upload_kb_file(self, local_file: Path) -> None:
        """
        Upload a local Knowledge_Base file to the corresponding Drive KB folder.
        Mirrors the local subfolder structure (e.g. Ideas/, Meetings/, etc.).
        """
        try:
            # Get the subfolder relative to local KB root (e.g. "Ideas", "Meetings")
            rel = local_file.relative_to(self.local_kb_dir)
            parts = rel.parts  # e.g. ("Ideas", "ideas.md")

            # Resolve or create the subfolder in Drive
            folder_id = self.kb_folder_id
            for part in parts[:-1]:  # all but the filename
                folder_id = self.drive_svc.get_or_create_subfolder(folder_id, part)

            self.drive_svc.upload_file(local_file, folder_id)
            print(f"[DriveAgent] Uploaded KB file: {'/'.join(parts)}")

        except Exception as e:
            print(f"[DriveAgent] Warning — could not upload {local_file.name}: {e}")

    # ── Archive phase ─────────────────────────────────────

    def move_to_processed(self, file_name: str) -> None:
        """Move the original MP3 in Drive from Inbox → Processed."""
        file_id = self._downloaded.get(file_name)
        if not file_id:
            return  # file wasn't from Drive, nothing to move

        try:
            self.drive_svc.move_file(file_id, self.processed_id)
            print(f"[DriveAgent] Moved in Drive: {file_name} -> Processed/")
        except Exception as e:
            print(f"[DriveAgent] Warning — could not move {file_name} in Drive: {e}")
