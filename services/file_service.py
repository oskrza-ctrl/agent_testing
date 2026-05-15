from pathlib import Path


def find_all_mp3(input_dir: Path) -> list:
    """Returns all MP3 files found in input_dir, sorted by name."""
    mp3_files = sorted(input_dir.glob("*.mp3"))

    if not mp3_files:
        print("No MP3 files found in input/")
    else:
        print(f"Found {len(mp3_files)} MP3 file(s): {[f.name for f in mp3_files]}")

    return mp3_files


def save_text(path: Path, content: str) -> None:
    """Saves text content to a file in UTF-8."""
    path.write_text(content, encoding="utf-8")
    print(f"Saved: {path}")
