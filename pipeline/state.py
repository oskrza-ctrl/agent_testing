from typing import TypedDict, Optional, Any


class PipelineState(TypedDict):
    mp3_path: Any          # Path object
    mp3_name: str          # "audio.mp3"
    mp3_stem: str          # "audio"
    transcript: str        # texto transcrito del audio
    result: Any            # AnalysisResult object (post-análisis)
    error: Optional[str]   # mensaje de error si algún nodo falla
