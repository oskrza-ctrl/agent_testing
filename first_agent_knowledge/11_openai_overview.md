---
tags: [openai, api, modelos, pricing]
---

# OpenAI API — overview

OpenAI es el proveedor de IA principal del proyecto. Se usa para dos tareas distintas: transcribir audio y analizar texto.

## Modelos usados en el proyecto

| Modelo | Tarea | Costo aproximado |
|--------|-------|-----------------|
| `whisper-1` | Transcripción de audio | ~$0.006 / minuto |
| `gpt-4o-mini` | Análisis de texto y clasificación | ~$0.15 / millón de tokens de entrada |

`gpt-4o` es ~16x más caro que `gpt-4o-mini` para la misma tarea de clasificación. Por eso se eligió `gpt-4o-mini`.

## Instalación y uso básico

```python
pip install openai
```

```python
import openai

client = openai.OpenAI(api_key="sk-proj-...")
```

El cliente se crea una vez y se reutiliza para todos los requests.

## Dos tipos de llamadas

**Audio (Whisper):**

```python
with open("audio.mp3", "rb") as f:
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=f
    )
transcript = response.text
```

**Chat / texto (GPT-4o-mini):**

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un clasificador de contenido..."},
        {"role": "user", "content": transcript}
    ],
    response_format={"type": "json_object"}
)
content = response.choices[0].message.content
```

## Tokens: la unidad de cobro

Los modelos de texto cobran por "tokens" — fragmentos de texto de ~4 caracteres promedio. Un transcript de 5 minutos puede generar ~1,000 tokens de entrada.

Con `gpt-4o-mini` a $0.15 / millón de tokens, 1,000 tokens cuestan $0.00015. Una sesión intensiva de 100 audios costaría centavos.

## Servicios intercambiables

La clase `OpenAITranscriptionService` implementa la interfaz `TranscriptionService`. Si en el futuro se migra a Whisper local, solo cambia la implementación — el pipeline no cambia.

```python
class OpenAITranscriptionService(TranscriptionService):
    def __init__(self, client, model: str = "whisper-1"):
        self.client = client
        self.model  = model

    def transcribe(self, audio_path: Path) -> str:
        with open(audio_path, "rb") as f:
            r = self.client.audio.transcriptions.create(
                model=self.model, file=f
            )
        return r.text
```

## Conceptos relacionados

- [[12_openai_whisper]] — transcripción de audio en detalle
- [[13_openai_gpt4o_mini]] — análisis de texto en detalle
- [[14_openai_json_mode]] — por qué se pide respuesta en JSON
- [[20_arquitectura_servicios]] — cómo se hace el servicio intercambiable
