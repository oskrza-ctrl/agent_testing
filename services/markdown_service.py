from pathlib import Path


def ensure_transcript(markdown: str, transcript: str) -> str:
    """Appends the full transcript to the markdown if it's not already included."""
    if transcript not in markdown:
        markdown += f"\n\n{transcript}"
    return markdown


def save_markdown(path: Path, content: str) -> None:
    """Saves markdown content to a file in UTF-8."""
    path.write_text(content, encoding="utf-8")
    print(f"Analysis saved to: {path}")
