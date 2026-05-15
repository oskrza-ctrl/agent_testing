from pathlib import Path


class ArchiveAgent:
    """Placeholder — will move processed files to Knowledge_Base/Processed/ in a future phase."""

    def run(self, mp3_path: Path) -> None:
        print(f"[ArchiveAgent] Skipping archive for: {mp3_path.name}")
