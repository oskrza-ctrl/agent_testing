import re
from datetime import date, datetime
from pathlib import Path

from services.analysis.analysis_result import AnalysisResult


# Categories that accumulate entries in a single file
ACCUMULATIVE = {
    "Idea":         ("Ideas",     "ideas.md",     "# Ideas\n\n"),
    "Tarea":        ("Tasks",     "tasks.md",      "# Tareas\n\n"),
    "Recordatorio": ("Reminders", "reminders.md",  "# Recordatorios\n\n"),
    "Proyecto":     ("Projects",  "projects.md",   "# Proyectos\n\n"),
}

# Categories that generate individual files
INDIVIDUAL = {"Reunion": "Meetings", "Nota general": "General_Notes"}

# Secondary-element routing map: list field -> (folder, filename, header)
SECONDARY_ROUTES = {
    "tasks":     ("Tasks",     "tasks.md",     "# Tareas\n\n"),
    "reminders": ("Reminders", "reminders.md", "# Recordatorios\n\n"),
    "ideas":     ("Ideas",     "ideas.md",     "# Ideas\n\n"),
}


class KnowledgeBaseAgent:
    """Routes an AnalysisResult to the correct location in Knowledge_Base/."""

    def __init__(self, kb_dir: Path):
        self.kb_dir = kb_dir
        self._init_dirs()

    def _init_dirs(self) -> None:
        folders = (
            [d for d, _, _ in ACCUMULATIVE.values()]
            + list(INDIVIDUAL.values())
        )
        for folder in folders:
            (self.kb_dir / folder).mkdir(parents=True, exist_ok=True)

    # ── Main entry point ─────────────────────────────────

    def run(self, result: AnalysisResult, source: str) -> None:
        # 1. Write primary entry
        if result.category in ACCUMULATIVE:
            folder, filename, header = ACCUMULATIVE[result.category]
            entry = self._build_entry(result, source)
            target = self.kb_dir / folder / filename
            self._append(target, entry, header)
        else:
            # Reunión or Nota general → individual file
            # Normalize category name for folder lookup
            folder_key = "Reunion" if result.category == "Reunión" else result.category
            folder = INDIVIDUAL.get(folder_key, "General_Notes")
            entry = (
                self._build_meeting_entry(result, source)
                if result.category in ("Reunión", "Reunion")
                else self._build_entry(result, source)
            )
            target = self.kb_dir / folder / self._make_filename(result.title)
            self._write_individual(target, entry)

        print(f"[KnowledgeBaseAgent] Primary -> {target}")

        # 2. Route secondary elements from Reunión / Nota general
        if result.category not in ACCUMULATIVE:
            self._route_secondary(result, source, str(target))

    # ── Entry builders ────────────────────────────────────

    def _build_entry(self, result: AnalysisResult, source: str) -> str:
        """Generic entry for Ideas, Tareas, Recordatorios, Proyectos, Nota general."""
        today = date.today().isoformat()

        def bullets(items: list) -> str:
            return "\n".join(f"- {item}" for item in items) if items else "No detectado"

        tags = " ".join(f"#{t.lstrip('#')}" for t in result.tags) if result.tags else "No detectado"

        return (
            f"## {today} — {result.title}\n\n"
            f"**Fuente:** {source}  \n"
            f"**Categoria:** {result.category}  \n"
            f"**Proyecto relacionado:** {result.related_project}  \n\n"
            f"**Resumen:**  \n{result.summary or 'No detectado'}\n\n"
            f"**Ideas detectadas:**  \n{bullets(result.ideas)}\n\n"
            f"**Tareas detectadas:**  \n{bullets(result.tasks)}\n\n"
            f"**Recordatorios:**  \n{bullets(result.reminders)}\n\n"
            f"**Requiere revision:**  \n{result.ambiguity_notes or 'Ninguno'}\n\n"
            f"**Tags:** {tags}\n"
        )

    def _build_meeting_entry(self, result: AnalysisResult, source: str) -> str:
        """Rich entry for Reunión with participants, decisions, and action sections."""
        today = date.today().isoformat()

        def bullets(items: list) -> str:
            return "\n".join(f"- {item}" for item in items) if items else "No detectado"

        tags = " ".join(f"#{t.lstrip('#')}" for t in result.tags) if result.tags else "No detectado"
        participants_str = ", ".join(result.participants) if result.participants else "No detectado"

        return (
            f"## {today} — {result.title}\n\n"
            f"**Fuente:** {source}  \n"
            f"**Participantes:** {participants_str}  \n"
            f"**Proyecto relacionado:** {result.related_project}  \n\n"
            f"**Resumen:**  \n{result.summary or 'No detectado'}\n\n"
            f"**Decisiones:**  \n{bullets(result.decisions)}\n\n"
            f"**Acciones para mi:**  \n{bullets(result.actions_for_me)}\n\n"
            f"**Acciones para otros:**  \n{bullets(result.actions_for_others)}\n\n"
            f"**Riesgos y bloqueos:**  \n{bullets(result.risks_blockers)}\n\n"
            f"**Proximos pasos:**  \n{bullets(result.next_steps)}\n\n"
            f"**Tareas detectadas:**  \n{bullets(result.tasks)}\n\n"
            f"**Recordatorios:**  \n{bullets(result.reminders)}\n\n"
            f"**Ideas detectadas:**  \n{bullets(result.ideas)}\n\n"
            f"**Requiere revision:**  \n{result.ambiguity_notes or 'Ninguno'}\n\n"
            f"**Tags:** {tags}\n"
        )

    # ── Secondary element routing ─────────────────────────

    def _route_secondary(self, result: AnalysisResult, source: str, origin_file: str) -> None:
        """Append tasks, reminders, and ideas from a Reunión/Nota general to their accumulative files."""
        field_map = {
            "tasks":     result.tasks,
            "reminders": result.reminders,
            "ideas":     result.ideas,
        }
        for field, items in field_map.items():
            if not items:
                continue
            folder, filename, header = SECONDARY_ROUTES[field]
            target = self.kb_dir / folder / filename
            entry = self._build_secondary_entry(items, field, source, origin_file)
            self._append(target, entry, header)
            print(f"[KnowledgeBaseAgent] Secondary ({field}) -> {target}")

    def _build_secondary_entry(
        self, items: list, field: str, source: str, origin_file: str
    ) -> str:
        today = date.today().isoformat()
        label = {"tasks": "Tarea", "reminders": "Recordatorio", "ideas": "Idea"}[field]
        bullets = "\n".join(f"- {item}" for item in items)
        return (
            f"## {today} — Elementos de: {source}\n\n"
            f"**Fuente:** {source}  \n"
            f"**Origen:** {origin_file}  \n\n"
            f"**{label}s detectados:**  \n{bullets}\n"
        )

    # ── File writers ──────────────────────────────────────

    def _append(self, path: Path, entry: str, header: str) -> None:
        if not path.exists():
            path.write_text(header + entry, encoding="utf-8")
        else:
            existing = path.read_text(encoding="utf-8")
            path.write_text(existing + "\n---\n\n" + entry, encoding="utf-8")

    def _write_individual(self, path: Path, entry: str) -> None:
        if path.exists():
            ts = datetime.now().strftime("%H%M%S")
            path = path.parent / f"{path.stem}_{ts}{path.suffix}"
        path.write_text(entry, encoding="utf-8")

    # ── Filename helper ───────────────────────────────────

    def _make_filename(self, title: str) -> str:
        today = date.today().isoformat()
        safe = re.sub(r"[^\w\s-]", "", title.lower())
        safe = re.sub(r"\s+", "_", safe.strip())
        safe = safe[:50].rstrip("_") or "sin_titulo"
        return f"{today}_{safe}.md"
