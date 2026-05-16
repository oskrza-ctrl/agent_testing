---
tags: [openai, whisper, transcripcion, audio]
---

# Transcripción de audio con Whisper-1

Whisper es el modelo de OpenAI para convertir audio en texto. Es el primer paso del pipeline: sin transcript, nada más puede funcionar.

## Por qué Whisper-1

- Costo: ~$0.006 por minuto de audio (muy económico para uso personal)
- Calidad: excelente en español, inglés y muchos idiomas
- Integración: una sola llamada API, sin configuración compleja
- Límite de archivo: 25 MB máximo (suficiente para audios de notas personales)

## Llamada a la API

```python
with open(audio_path, "rb") as audio_file:
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        # language="es"  # opcional — Whisper lo detecta automáticamente
    )

transcript = response.text
# "Hola, quiero capturar una idea sobre automatizar el inbox..."
```

## Implementación en el proyecto

`TranscriptionAgent` envuelve a `OpenAITranscriptionService`:

```python
class TranscriptionAgent:
    def __init__(self, service: TranscriptionService):
        self.service = service

    def run(self, audio_path: Path) -> str:
        print(f"[TranscriptionAgent] Transcribing: {audio_path.name}")
        transcript = self.service.transcribe(audio_path)
        print(f"[TranscriptionAgent] Done ({len(transcript)} chars)")
        return transcript
```

El transcript se guarda en `output/{stem}_transcript.txt` como respaldo.

## Limitaciones y plan futuro

- **Costo escala con volumen**: 100 horas de audio = $36 USD. Para uso intensivo, migrar a Whisper local (modelo open-source) elimina el costo.
- **La decisión DEC-002** documenta esta ruta: usar `whisper-1` ahora, migrar a Whisper local en Fase 1.5.

La arquitectura de servicios intercambiables hace que esta migración sea mínima: solo se crea `LocalWhisperTranscriptionService` implementando la misma interfaz.

## Conceptos relacionados

- [[11_openai_overview]] — pricing y SDK de OpenAI
- [[20_arquitectura_servicios]] — interfaz TranscriptionService
- [[13_openai_gpt4o_mini]] — el siguiente paso después del transcript
