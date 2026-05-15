import hashlib
import json
import re
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Optional

from services.analysis.analysis_result import AnalysisResult
from services.calendar.base import CalendarService


_CALENDAR_MARKER = "[candidato: google calendar]"

_DAYS = {
    "lunes": 0, "martes": 1,
    "miercoles": 2, "miércoles": 2,
    "jueves": 3, "viernes": 4,
    "sabado": 5, "sábado": 5, "domingo": 6,
}

_EVENT_DURATION_HOURS = 1


class CalendarAgent:
    """
    Creates Google Calendar events from reminders marked [candidato: Google Calendar].

    Rule: only reminders with explicit date AND time become events.
    If date or time cannot be parsed, the reminder is skipped.
    """

    def __init__(self, calendar_svc: CalendarService, tracking_file: Path):
        self.calendar_svc  = calendar_svc
        self.tracking_file = tracking_file
        self._tracking     = self._load_tracking()

    # ── Main entry point ──────────────────────────────────

    def run(self, result: AnalysisResult, source: str) -> None:
        created = 0
        prefix = self._project_prefix(result.related_project)

        for reminder_text in result.reminders:
            if _CALENDAR_MARKER not in reminder_text.lower():
                continue

            event_date = self._resolve_date(reminder_text)
            event_time = self._extract_time(reminder_text)

            if not event_date or not event_time:
                print(f"[CalendarAgent] Cannot parse date/time, skipping: '{reminder_text[:60]}'")
                continue

            # Use result.title as event title — already clean and descriptive
            title = (prefix + result.title)[:255]
            start = datetime.combine(event_date, event_time)
            end   = start + timedelta(hours=_EVENT_DURATION_HOURS)
            description = f"{result.summary}\n\nFuente: {source}"

            if self._create_if_new(title, source, result.summary, start, end):
                created += 1

        if created == 0:
            print("[CalendarAgent] No new events created.")
        else:
            print(f"[CalendarAgent] {created} event(s) created in Google Calendar.")

    # ── Date / time helpers ───────────────────────────────

    def _resolve_date(self, text: str) -> Optional[date]:
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

        return None

    def _extract_time(self, text: str) -> Optional[time]:
        lower = text.lower()

        # "a las HH:MM"
        m = re.search(r"a las (\d{1,2}):(\d{2})", lower)
        if m:
            return time(int(m.group(1)), int(m.group(2)))

        # "a las H pm/am" — with optional dot notation
        m = re.search(r"a las (\d{1,2})\s*p\.?m\.?", lower)
        if m:
            h = int(m.group(1))
            return time(h + 12 if h < 12 else h, 0)

        m = re.search(r"a las (\d{1,2})\s*a\.?m\.?", lower)
        if m:
            h = int(m.group(1))
            return time(0 if h == 12 else h, 0)

        # standalone "7 pm" / "7pm" / "7 p.m."
        m = re.search(r"(\d{1,2})\s*p\.?m\.?", lower)
        if m:
            h = int(m.group(1))
            return time(h + 12 if h < 12 else h, 0)

        m = re.search(r"(\d{1,2})\s*a\.?m\.?", lower)
        if m:
            h = int(m.group(1))
            return time(0 if h == 12 else h, 0)

        # 24-hour "19:00"
        m = re.search(r"\b(\d{1,2}):(\d{2})\b", lower)
        if m:
            return time(int(m.group(1)), int(m.group(2)))

        return None

    # ── Title helpers ─────────────────────────────────────

    def _project_prefix(self, related_project: str) -> str:
        if related_project and related_project.lower() != "no asignado":
            return f"[{related_project}] "
        return ""

    def _clean(self, text: str) -> str:
        text = re.sub(r"\[candidato:.*?\]", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\(.*?\)", "", text)
        text = re.sub(r"—.*$", "", text)
        return text.strip(" -–—")[:255]

    # ── Deduplication ─────────────────────────────────────

    def _event_hash(self, source: str, title: str) -> str:
        return hashlib.sha256(f"{source}:{title}".lower().encode()).hexdigest()[:16]

    def _create_if_new(
        self,
        title: str,
        source: str,
        description: str,
        start: datetime,
        end: datetime,
    ) -> bool:
        h = self._event_hash(source, title)
        if any(e["hash"] == h for e in self._tracking):
            print(f"[CalendarAgent] Duplicate skipped: '{title[:60]}'")
            return False

        event_id = self.calendar_svc.create_event(
            title=title, start=start, end=end,
            description=f"{description}\n\nFuente: {source}"
        )
        print(f"[CalendarAgent] Created: '{title[:60]}' — {start.strftime('%Y-%m-%d %H:%M')}")

        self._tracking.append({
            "hash":             h,
            "source":           source,
            "title":            title,
            "google_event_id":  event_id,
            "start":            start.isoformat(),
            "created_at":       date.today().isoformat(),
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
