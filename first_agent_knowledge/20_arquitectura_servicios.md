---
tags: [arquitectura, servicios, intercambiables, patrones, abc]
---

# Arquitectura de servicios intercambiables

El proyecto está diseñado para que el proveedor de cada servicio (transcripción, análisis) pueda cambiarse sin modificar el pipeline. Se logra usando clases base abstractas como interfaces.

## El problema que resuelve

Sin esta arquitectura:

```python
# En orchestrator_agent.py — acoplado a OpenAI
import openai
transcript = openai.audio.transcriptions.create(model="whisper-1", file=f)
```

Si quieres cambiar a Whisper local, debes modificar el orchestrator y encontrar todos los lugares donde se llama a OpenAI.

## La solución: interfaces abstractas

```python
# services/transcription/base.py
from abc import ABC, abstractmethod
from pathlib import Path

class TranscriptionService(ABC):
    @abstractmethod
    def transcribe(self, audio_path: Path) -> str:
        ...
```

```python
# services/transcription/openai_transcription.py
class OpenAITranscriptionService(TranscriptionService):
    def transcribe(self, audio_path: Path) -> str:
        with open(audio_path, "rb") as f:
            r = self.client.audio.transcriptions.create(
                model=self.model, file=f
            )
        return r.text
```

```python
# En el futuro:
class LocalWhisperTranscriptionService(TranscriptionService):
    def transcribe(self, audio_path: Path) -> str:
        # usar modelo local sin costo de API
        ...
```

## Cómo el orchestrator usa la interfaz

```python
class TranscriptionAgent:
    def __init__(self, service: TranscriptionService):  # ← acepta CUALQUIER implementación
        self.service = service

    def run(self, audio_path: Path) -> str:
        return self.service.transcribe(audio_path)
```

Para cambiar el proveedor, solo se cambia `main.py`:

```python
# Hoy:
transcription_svc = OpenAITranscriptionService(client)

# Mañana:
transcription_svc = LocalWhisperTranscriptionService()
```

El resto del código no cambia.

## Servicios definidos en el proyecto

| Interfaz | Implementación actual | Implementación futura |
|----------|----------------------|----------------------|
| `TranscriptionService` | `OpenAITranscriptionService` | `LocalWhisperTranscriptionService` |
| `AnalysisService` | `OpenAIAnalysisService` | `LocalModelAnalysisService` |
| `TasksService` | `GoogleTasksService` | Cualquier gestor de tareas |
| `CalendarService` | `GoogleCalendarService` | Cualquier servicio de calendario |

## Conceptos relacionados

- [[03_python_clases_oop]] — clases base abstractas (ABC)
- [[21_arquitectura_agentes]] — cómo los agentes usan los servicios
- [[11_openai_overview]] — la implementación actual de transcripción y análisis
