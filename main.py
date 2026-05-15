from dotenv import load_dotenv
from pathlib import Path
import os

from services.transcription.openai_transcription import OpenAITranscriptionService
from services.analysis.openai_analysis import OpenAIAnalysisService
from agents.orchestrator_agent import OrchestratorAgent

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("OPENAI_API_KEY not found")
    exit(1)

print("API key loaded successfully")

transcription_svc = OpenAITranscriptionService(api_key)
analysis_svc      = OpenAIAnalysisService(api_key)

credentials_file = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials/credentials.json"))

# ── Google Tasks ──────────────────────────────────────
tasks_svc  = None
token_file = Path(os.getenv("GOOGLE_TOKEN_FILE", "credentials/token.json"))
if credentials_file.exists():
    from services.tasks.google_tasks_service import GoogleTasksService
    tasks_svc = GoogleTasksService(credentials_file, token_file)
    print("Google Tasks: enabled.")
else:
    print("Google Tasks: credentials not found, skipping.")

# ── Google Calendar ───────────────────────────────────
calendar_svc      = None
cal_token_file    = Path(os.getenv("GOOGLE_CALENDAR_TOKEN_FILE", "credentials/token_calendar.json"))
calendar_timezone = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "America/Mexico_City")
if credentials_file.exists():
    from services.calendar.google_calendar_service import GoogleCalendarService
    calendar_svc = GoogleCalendarService(credentials_file, cal_token_file, calendar_timezone)
    print("Google Calendar: enabled.")
else:
    print("Google Calendar: credentials not found, skipping.")

# ── Google Drive ──────────────────────────────────────
drive_agent      = None
drive_token_file = Path(os.getenv("GOOGLE_DRIVE_TOKEN_FILE", "credentials/token_drive.json"))
inbox_id         = os.getenv("GOOGLE_DRIVE_INBOX_FOLDER_ID", "")
processed_id     = os.getenv("GOOGLE_DRIVE_PROCESSED_FOLDER_ID", "")
kb_id            = os.getenv("GOOGLE_DRIVE_KB_FOLDER_ID", "")

if credentials_file.exists() and inbox_id and processed_id and kb_id:
    from services.drive.google_drive_service import GoogleDriveService
    from agents.drive_agent import DriveAgent
    drive_svc   = GoogleDriveService(credentials_file, drive_token_file)
    drive_agent = DriveAgent(
        drive_svc=drive_svc,
        inbox_folder_id=inbox_id,
        processed_folder_id=processed_id,
        kb_folder_id=kb_id,
        local_input_dir=Path("input"),
        local_kb_dir=Path("Knowledge_Base"),
    )
    print("Google Drive: enabled.")
else:
    print("Google Drive: not configured, using local folders only.")

orchestrator = OrchestratorAgent(
    transcription_svc=transcription_svc,
    analysis_svc=analysis_svc,
    input_dir=Path("input"),
    output_dir=Path("output"),
    processed_dir=Path("processed"),
    prompts_dir=Path("prompts"),
    kb_dir=Path("Knowledge_Base"),
    tasks_svc=tasks_svc,
    calendar_svc=calendar_svc,
    drive_agent=drive_agent,
)

orchestrator.run()
