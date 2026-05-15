import hashlib
import json
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

from services.analysis.analysis_result import AnalysisResult
from services.tasks.base import TasksService


# Markers injected by the analysis prompt
_CALENDAR_MARKER = "[candidato: google calendar]"
_TASKS_MARKER    = "[candidato: google tasks]"
_REVIEW_MARKERS  = ["requiere revision", "requiere revisión"]

# Spanish day names → weekday index (Monday=0)
_DAYS = {
    "lunes": 0, "martes": 1,
    "miercoles": 2, "miércoles": 2,
    "jueves": 3, "viernes": 4,
    "sabado": 5, "sábado": 5, "domingo": 6,
}


class TasksAgent:
    """
    Applies routing rules and creates Google Tasks from an AnalysisResult.

    Rules:
      tasks[]   — clear without date  → Google Task (no due date)
      tasks[]   — clear with date     → Google Task with due date
      tasks[]   — ambiguous/review    → skip (Markdown only)
      reminders — [candidato: Google Tasks]    → Google Task with due date
      reminders — [candidato: Google Calendar] → skip (reserved for Calendar)
      reminders — no marker / ambiguous        → skip
    """

    def __init__(self, tasks_svc: TasksService, tracking_file: Path):
        self.tasks_svc     = tasks_svc
        self.tracking_file = tracking_file
        self._tracking     = self._load_tracking()

    # ── Main entry point ──────────────────────────────────

    def run(self, result: AnalysisResult, source: str) -> None:
        created = 0

        prefix = self._project_prefix(result.related_project)

        for task_text in result.tasks:
            if self._is_ambiguous(task_text):
                print(f"[TasksAgent] Skipping ambiguous task: '{task_text[:60]}'")
                continue
            due   = self._resolve_date(task_text)
            title = prefix + self._clean(task_text)
            if self._create_if_new(title, source, result.summary, due):
                created += 1

        for reminder_text in result.reminders:
            lower = reminder_text.lower()
            if _CALENDAR_MARKER in lower:
                continue  # reserved for Google Calendar
            if _TASKS_MARKER not in lower:
                continue  # ambiguous, skip
            due   = self._resolve_date(reminder_text)
            title = prefix + self._clean(reminder_text)
            if self._create_if_new(title, source, result.summary, due):
                created += 1

        if created == 0:
            print("[TasksAgent] No new tasks created.")
        else:
            print(f"[TasksAgent] {created} task(s) created in Google Tasks.")

    # ── Routing helpers ───────────────────────────────────

    def _is_ambiguous(self, text: str) -> bool:
        lower = text.lower()
        return any(m in lower for m in _REVIEW_MARKERS)

    def _resolve_date(self, text: str) -> Optional[date]:
        """Extract a due date from a task/reminder string. Returns None if no date found."""
        today = date.today()
        lower = text.lower()

        if "pasado mañana" in lower or "pasado manana" in lower:
            return today + timedelta(days=2)
        if "mañana" in lower or "manana" in lower:
            return today + timedelta(days=1)

        for name, idx in _DAYS.items():
            if name in lower:
                ahead = idx - today.weekday()
                if ahead <= 0:
                    ahead += 7
                return today + timedelta(days=ahead)

        # No date found — default to 7 days so tasks don't float indefinitely
        return today + timedelta(days=7)

    def _project_prefix(self, related_project: str) -> str:
        """Return '[Proyecto] ' prefix if a real project is assigned."""
        if related_project and related_project.lower() != "no asignado":
            return f"[{related_project}] "
        return ""

    def _clean(self, text: str) -> str:
        """Strip markers and date hints from the task title."""
        text = re.sub(r"\[candidato:.*?\]", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\(.*?\)", "", text)
        text = re.sub(r"—.*$", "", text)
        return text.strip(" -–—")[:255]  # Google Tasks title limit

    # ── Deduplication ─────────────────────────────────────

    def _task_hash(self, source: str, title: str) -> str:
        return hashlib.sha256(f"{source}:{title}".lower().encode()).hexdigest()[:16]

    def _create_if_new(
        self, title: str, source: str, notes: str, due_date: Optional[date]
    ) -> bool:
        h = self._task_hash(source, title)
        if any(e["hash"] == h for e in self._tracking):
            print(f"[TasksAgent] Duplicate skipped: '{title[:60]}'")
            return False

        task_id = self.tasks_svc.create_task(title=title, notes=notes, due_date=due_date)
        due_str = str(due_date) if due_date else "sin fecha"
        print(f"[TasksAgent] Created: '{title[:60]}' — {due_str}")

        self._tracking.append({
            "hash":           h,
            "source":         source,
            "task_text":      title,
            "google_task_id": task_id,
            "created_at":     date.today().isoformat(),
        })
        self._save_tracking()
        return True

    # ── Tracking file ─────────────────────────────────────

    def _load_tracking(self) -> list:
        if self.tracking_file.exists():
            return json.loads(self.tracking_file.read_text(encoding="utf-8"))
        return []

    def _save_tracking(self) -> None:
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)
        self.tracking_file.write_text(
            json.dumps(self._tracking, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
