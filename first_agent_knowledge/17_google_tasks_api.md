---
tags: [google, tasks, api, tareas, integracion]
---

# Google Tasks API

Google Tasks permite crear y gestionar listas de tareas desde código. El proyecto la usa para crear automáticamente tareas cuando detecta acciones pendientes en los audios.

## Crear una lista y agregar tareas

```python
from googleapiclient.discovery import build

service = build("tasks", "v1", credentials=creds)

# Crear una lista dedicada (si no existe)
task_list = service.tasklists().insert(body={"title": "Second Brain Agent"}).execute()
tasklist_id = task_list["id"]

# Crear una tarea en esa lista
task_body = {
    "title": "[BOYA] Revisar el contrato",
    "notes": "Detectado en audio del 2026-05-15",
    "due": "2026-05-22T00:00:00.000Z",   # RFC 3339
}
task = service.tasks().insert(
    tasklist=tasklist_id,   # IMPORTANTE: es "tasklist", no "tasklistId"
    body=task_body
).execute()
```

**Error frecuente**: el parámetro correcto es `tasklist=` no `tasklistId=`. La documentación de Google es inconsistente en este punto.

## Organización: una lista "Second Brain Agent"

En lugar de mezclar las tareas con otras listas de Google Tasks, el proyecto crea una lista dedicada llamada "Second Brain Agent". Al arrancar, verifica si ya existe:

```python
def _find_or_create_list(self, service) -> str:
    result = service.tasklists().list().execute()
    for tl in result.get("items", []):
        if tl["title"] == "Second Brain Agent":
            return tl["id"]
    new_list = service.tasklists().insert(
        body={"title": "Second Brain Agent"}
    ).execute()
    return new_list["id"]
```

## Reglas de creación de tareas

| Situación | Acción |
|-----------|--------|
| Tarea clara sin fecha | Task con due date = hoy + 7 días |
| Tarea con fecha relativa ("mañana") | Task con due date calculado |
| Recordatorio con `[candidato: Google Tasks]` | Task con due date |
| Recordatorio con `[candidato: Google Calendar]` | Saltado — lo maneja CalendarAgent |
| Ambiguo / "requiere revision" | Solo Markdown, no se crea task |

## Prefijo de proyecto en el título

```python
def _project_prefix(self, related_project: str) -> str:
    if related_project and related_project.lower() != "no asignado":
        return f"[{related_project}] "
    return ""
```

Resultado: `"[BOYA] Revisar el contrato"` — el proyecto es visible de un vistazo.

## Conceptos relacionados

- [[27_reglas_calendario_tareas]] — lógica de cuándo crear task vs event
- [[26_deduplicacion]] — cómo se evita crear la misma tarea dos veces
- [[16_google_oauth2]] — autenticación para la API
