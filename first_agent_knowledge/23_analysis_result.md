---
tags: [dataclass, analysis-result, estructura-datos, json]
---

# AnalysisResult — estructura de datos central

`AnalysisResult` es el dataclass que representa el output del análisis de un audio. Todos los agentes posteriores (KB, Tasks, Calendar, Drive) reciben este objeto y actúan sobre él.

## Definición completa

```python
@dataclass
class AnalysisResult:
    category: str           # Categoría principal del contenido
    title: str              # Título limpio para el archivo
    summary: str            # Resumen en 2-3 oraciones
    ideas: List[str]        # Ideas detectadas en el audio
    tasks: List[str]        # Tareas accionables
    reminders: List[str]    # Recordatorios con referencia temporal
    related_project: str    # "BOYA", "SAT" o "No asignado"
    ambiguity_notes: str    # Cosas ambiguas que requieren revisión humana
    tags: List[str]         # Mínimo 2 tags (#proyecto, #reunion, etc.)
    participants: List[str] # Personas mencionadas (para Reuniones)
    decisions: List[str]    # Acuerdos o conclusiones
    actions_for_me: List[str]    # Acciones para quien grabó
    actions_for_others: List[str]# Acciones para otras personas
    risks_blockers: List[str]    # Riesgos o bloqueos detectados
    next_steps: List[str]        # Próximos pasos
```

## Cómo se construye — desde el JSON de OpenAI

```python
data = json.loads(response.choices[0].message.content)

result = AnalysisResult(
    category=data.get("category", "Nota general"),
    title=data.get("title", "Sin título"),
    summary=data.get("summary", ""),
    ideas=data.get("ideas", []),
    tasks=data.get("tasks", []),
    reminders=data.get("reminders", []),
    related_project=data.get("related_project", "No asignado"),
    ambiguity_notes=data.get("ambiguity_notes", ""),
    tags=data.get("tags", ["#nota-general", "#sin-proyecto"]),
    participants=data.get("participants", []),
    decisions=data.get("decisions", []),
    actions_for_me=data.get("actions_for_me", []),
    actions_for_others=data.get("actions_for_others", []),
    risks_blockers=data.get("risks_blockers", []),
    next_steps=data.get("next_steps", []),
)
```

## Quién usa qué campo

| Agente | Campos que usa |
|--------|---------------|
| `KnowledgeBaseAgent` | todos |
| `TasksAgent` | `tasks`, `reminders`, `related_project`, `summary` |
| `CalendarAgent` | `reminders`, `title` |
| `DriveAgent` | `category`, `title`, `tasks`, `reminders`, `ideas` |

## El campo category — valores posibles

```
"Idea"
"Reunión"
"Tarea"
"Recordatorio"
"Proyecto"
"Nota general"
```

Este valor determina a qué carpeta de la Knowledge Base va el contenido.

## Conceptos relacionados

- [[24_categorias_contenido]] — las 6 categorías y cuándo se asigna cada una
- [[25_knowledge_base]] — cómo el category determina el enrutado
- [[07_python_dataclasses_typeddict]] — qué es un @dataclass
- [[14_openai_json_mode]] — de dónde viene el JSON que se parsea
