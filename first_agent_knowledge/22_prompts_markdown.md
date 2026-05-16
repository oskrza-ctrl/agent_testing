---
tags: [prompts, markdown, llm, instrucciones, analisis]
---

# Sistema de prompts en Markdown

En lugar de hardcodear las instrucciones del LLM en el código Python, el proyecto las guarda en archivos `.md` dentro de `prompts/`. Esto hace que el prompt sea fácil de editar, versionar y leer.

## Estructura de la carpeta

```
prompts/
├── analysis_agent.md     ← el más importante: clasifica y extrae datos
├── transcription_agent.md
├── markdown_agent.md
├── archive_agent.md
└── orchestrator_agent.md
```

## El PromptLoader

```python
# services/prompt_loader.py

def load_prompt(prompts_dir: Path, filename: str) -> str:
    path = prompts_dir / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt no encontrado: {path}\n"
            f"Disponibles: {list(prompts_dir.glob('*.md'))}"
        )
    return path.read_text(encoding="utf-8")
```

El error es claro: dice exactamente qué archivo falta y qué archivos sí existen.

## Cómo lo usa el AnalysisAgent

```python
class AnalysisAgent:
    def __init__(self, service: AnalysisService, prompts_dir: Path):
        self.service = service
        # Carga el prompt al inicializarse — una sola vez
        self.system_prompt = load_prompt(prompts_dir, "analysis_agent.md")

    def run(self, transcript: str) -> AnalysisResult:
        full_prompt = self.system_prompt + "\n\n---\n\nTranscript:\n" + transcript
        return self.service.analyze(full_prompt)
```

El prompt se carga **una vez** al iniciar, no en cada llamada. Así si el archivo no existe, el error aparece al arrancar, no a mitad de un batch.

## Estructura del analysis_agent.md

El prompt define:
- Las 6 categorías con criterios de clasificación
- El schema JSON exacto con los 15 campos
- La regla de no inventar fechas absolutas
- Los marcadores `[candidato: Google Calendar]` y `[candidato: Google Tasks]`
- Los tags de fallback cuando no hay tags específicos

```markdown
# Analysis Agent

Eres un agente de clasificación y extracción de información...

## Categorías

| Categoría | Cuándo usarla |
|-----------|--------------|
| Idea | Cuando el contenido es una idea o concepto... |
| Reunión | Cuando describe una reunión con participantes... |
...

## Regla de fechas

NUNCA conviertas referencias relativas ("mañana", "el viernes") en fechas absolutas.
Preserva el texto original...

## JSON de salida

Responde SIEMPRE con este JSON:
{"category": "...", "title": "...", ...}
```

## Por qué Markdown y no Python

- El prompt se puede editar sin tocar código
- Es fácil de leer y revisar (sin concatenaciones de strings)
- Se puede versionar en git con diffs legibles

## Conceptos relacionados

- [[13_openai_gpt4o_mini]] — dónde se usa el prompt
- [[24_categorias_contenido]] — las categorías definidas en el prompt
- [[14_openai_json_mode]] — el schema JSON que define el prompt
