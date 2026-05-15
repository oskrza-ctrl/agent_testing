from pathlib import Path

from services.markdown_service import ensure_transcript, save_markdown


class MarkdownAgent:
    """Ensures the Markdown is complete and saves it to output/."""

    def run(self, output_dir: Path, stem: str, transcript: str, markdown: str) -> None:
        markdown = ensure_transcript(markdown, transcript)
        save_markdown(output_dir / f"{stem}_analysis.md", markdown)
