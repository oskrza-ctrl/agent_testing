import shutil
from datetime import datetime
from pathlib import Path


class ArchiveAgent:
    """Moves a processed MP3 to the processed/ folder."""

    def __init__(self, processed_dir: Path):
        self.processed_dir = processed_dir

    def run(self, mp3_path: Path) -> None:
        self.processed_dir.mkdir(exist_ok=True)

        dest = self.processed_dir / mp3_path.name

        # Avoid overwriting: add timestamp if file already exists
        if dest.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = self.processed_dir / f"{mp3_path.stem}_{timestamp}{mp3_path.suffix}"

        shutil.move(str(mp3_path), str(dest))
        print(f"[ArchiveAgent] Moved to: {dest}")
