from openai import OpenAI


PROMPT_TEMPLATE = """Analiza el siguiente transcript de audio y genera un documento Markdown con estas secciones exactas.
Si no detectas información para una sección, escribe "No detectado". No inventes información.

Transcript:
{transcript}

Responde SOLO con el contenido Markdown, sin explicaciones adicionales.

# Título sugerido

## Resumen

## Ideas detectadas

## Tareas accionables

## Proyectos relacionados

## Recordatorios

## Tags

## Transcript completo
"""


def analyze(client: OpenAI, transcript: str) -> str:
    """Sends the transcript to GPT-4o-mini and returns the analysis as a Markdown string."""
    print("\nAnalyzing transcript...")

    prompt = PROMPT_TEMPLATE.format(transcript=transcript)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
