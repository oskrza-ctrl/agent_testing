from pathlib import Path

from services.analysis.analysis_result import AnalysisResult
from services.markdown_service import save_markdown


class MarkdownAgent:
    """Builds a structured Markdown document from an AnalysisResult and saves it."""

    def run(self, output_dir: Path, stem: str, transcript: str, result: AnalysisResult) -> None:
        markdown = self._build(result, transcript)
        save_markdown(output_dir / f"{stem}_analysis.md", markdown)

    def _build(self, result: AnalysisResult, transcript: str) -> str:
        def bullet_list(items: list) -> str:
            return "\n".join(f"- {item}" for item in items) if items else "No detectado"

        tags = " ".join(f"#{t.lstrip('#')}" for t in result.tags) if result.tags else "No detectado"

        # Optional sections — only rendered when there is content
        participants_section = (
            f"\n## Participantes\n\n{bullet_list(result.participants)}\n"
            if result.participants else ""
        )
        decisions_section = (
            f"\n## Decisiones\n\n{bullet_list(result.decisions)}\n"
            if result.decisions else ""
        )
        actions_for_me_section = (
            f"\n## Acciones para mi\n\n{bullet_list(result.actions_for_me)}\n"
            if result.actions_for_me else ""
        )
        actions_for_others_section = (
            f"\n## Acciones para otros\n\n{bullet_list(result.actions_for_others)}\n"
            if result.actions_for_others else ""
        )
        risks_section = (
            f"\n## Riesgos y bloqueos\n\n{bullet_list(result.risks_blockers)}\n"
            if result.risks_blockers else ""
        )
        next_steps_section = (
            f"\n## Proximos pasos\n\n{bullet_list(result.next_steps)}\n"
            if result.next_steps else ""
        )

        return (
            f"# {result.title}\n\n"
            f"## Categoria principal\n\n{result.category}\n"
            f"{participants_section}"
            f"\n## Resumen\n\n{result.summary or 'No detectado'}\n"
            f"{decisions_section}"
            f"{actions_for_me_section}"
            f"{actions_for_others_section}"
            f"{risks_section}"
            f"{next_steps_section}"
            f"\n## Ideas detectadas\n\n{bullet_list(result.ideas)}\n"
            f"\n## Tareas accionables\n\n{bullet_list(result.tasks)}\n"
            f"\n## Recordatorios\n\n{bullet_list(result.reminders)}\n"
            f"\n## Proyecto relacionado\n\n{result.related_project}\n"
            f"\n## Requiere revision\n\n{result.ambiguity_notes or 'Ninguno'}\n"
            f"\n## Tags\n\n{tags}\n"
            f"\n## Transcript completo\n\n{transcript}\n"
        )
