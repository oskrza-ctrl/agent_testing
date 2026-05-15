from pathlib import Path


def find_mp3(input_dir: Path) -> Path:
    """Returns the first MP3 found in input_dir, or exits if none."""
    mp3_files = list(input_dir.glob("*.mp3"))

    if not mp3_files:
        print("No MP3 files found in input/")
        exit(1)

    mp3_path = mp3_files[0]
    print(f"MP3 file found: {mp3_path.name}")
    return mp3_path


def save_text(path: Path, content: str) -> None:
    """Saves text content to a file in UTF-8."""
    path.write_text(content, encoding="utf-8")
    print(f"Saved: {path}")
