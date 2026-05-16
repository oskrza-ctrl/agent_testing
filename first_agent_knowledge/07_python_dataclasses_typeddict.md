---
tags: [python, fundamentos, dataclasses, typeddict, tipos]
---

# Dataclasses y TypedDict en Python

Cuando los datos tienen una estructura fija y conocida, Python ofrece dos herramientas: `@dataclass` para objetos con comportamiento y `TypedDict` para diccionarios tipados.

## @dataclass

Genera automáticamente `__init__`, `__repr__` y más a partir de los campos declarados.

```python
from dataclasses import dataclass
from typing import List

@dataclass
class AnalysisResult:
    category: str           # "Idea", "Reunión", "Tarea", etc.
    title: str              # título sugerido para el archivo
    summary: str            # resumen breve
    ideas: List[str]        # ideas detectadas
    tasks: List[str]        # tareas accionables
    reminders: List[str]    # recordatorios con referencia temporal
    related_project: str    # "BOYA" o "No asignado"
    ambiguity_notes: str    # elementos que requieren revisión
    tags: List[str]         # mínimo 2 tags
    participants: List[str]
    decisions: List[str]
    actions_for_me: List[str]
    actions_for_others: List[str]
    risks_blockers: List[str]
    next_steps: List[str]
```

Se instancia así:

```python
result = AnalysisResult(
    category="Idea",
    title="Automatizar el inbox",
    summary="Procesamiento automático de audios desde Drive",
    ideas=["Conectar con Cloud Run"],
    tasks=[],
    reminders=[],
    ...
)
```

## TypedDict

Un `TypedDict` es un diccionario con tipos declarados. LangGraph lo usa para el estado compartido del pipeline.

```python
from typing import TypedDict, Optional, Any

class PipelineState(TypedDict):
    mp3_path:   Any           # Path object
    mp3_name:   str           # "audio.mp3"
    mp3_stem:   str           # "audio"
    transcript: str           # texto transcrito
    result:     Any           # AnalysisResult (post-análisis)
    error:      Optional[str] # None si todo OK
```

La diferencia con `@dataclass`: un `TypedDict` es solo un diccionario con hints de tipo. No tiene métodos, no tiene constructor propio. LangGraph puede hacer merge de dos `TypedDict` parciales, lo que no se puede con un dataclass.

## type hints en funciones

```python
from typing import Optional
from datetime import date

def _resolve_date(self, text: str) -> Optional[date]:
    """Devuelve una fecha o None si no encuentra referencia temporal."""
    ...
```

Los type hints son documentación ejecutable — no fuerzan el tipo en tiempo de ejecución, pero los editores y herramientas de análisis los usan.

## Conceptos relacionados

- [[23_analysis_result]] — AnalysisResult completo con los 15 campos
- [[30_langgraph_stategraph]] — PipelineState como estado del grafo
- [[03_python_clases_oop]] — diferencia entre @dataclass y clase regular
