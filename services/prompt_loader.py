from pathlib import Path


def load_prompt(prompts_dir: Path, filename: str) -> str:
    """Read a prompt file from prompts_dir. Raises FileNotFoundError with a clear message."""
    path = prompts_dir / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {path}\n"
            f"Create '{filename}' inside '{prompts_dir}/' before running."
        )
    return path.read_text(encoding="utf-8")
