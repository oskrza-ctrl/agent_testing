from openai import OpenAI

from services.analysis.base import AnalysisService


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


class OpenAIAnalysisService(AnalysisService):
    """Text analysis using OpenAI GPT-4o-mini."""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze(self, transcript: str) -> str:
        print("\nAnalyzing transcript...")

        prompt = PROMPT_TEMPLATE.format(transcript=transcript)

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content
