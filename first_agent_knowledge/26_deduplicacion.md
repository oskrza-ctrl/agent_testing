---
tags: [deduplicacion, hash, json, tareas, calendario]
---

# Deduplicación — evitar crear dos veces lo mismo

Si el mismo MP3 se procesa dos veces, o dos audios mencionan la misma tarea, el sistema no debe crear duplicados en Google Tasks ni en Google Calendar. Se usa un hash SHA256 para identificar entradas únicas.

## El problema

Sin deduplicación, procesar el mismo audio dos veces crea la misma tarea dos veces en Google Tasks. Procesar 10 audios que mencionan "Llamar al banco" crea 10 tareas idénticas.

## La solución: hash + archivo JSON

```python
import hashlib
import json

def _task_hash(self, source: str, title: str) -> str:
    return hashlib.sha256(
        f"{source}:{title}".lower().encode()
    ).hexdigest()[:16]
```

La clave única es `{source}:{title}` donde:
- `source` = nombre del MP3 (ej: `reunion_boya.mp3`)
- `title` = título limpio de la tarea (ej: `[BOYA] Revisar el contrato`)

El hash se trunca a 16 caracteres — suficiente para evitar colisiones en un uso personal.

## Archivo de tracking

```json
// Knowledge_Base/Tasks/created_tasks.json
[
  {
    "hash": "a1b2c3d4e5f6a7b8",
    "source": "reunion_boya.mp3",
    "task_text": "[BOYA] Revisar el contrato",
    "google_task_id": "abc123xyz",
    "created_at": "2026-05-15"
  }
]
```

Antes de crear una tarea, se verifica si el hash ya existe:

```python
def _create_if_new(self, title, source, notes, due_date) -> bool:
    h = self._task_hash(source, title)
    if any(e["hash"] == h for e in self._tracking):
        print(f"[TasksAgent] Duplicate skipped: '{title[:60]}'")
        return False
    # Crear la tarea...
    self._tracking.append({...})
    self._save_tracking()
    return True
```

## Archivos de tracking del proyecto

| Archivo | Uso |
|---------|-----|
| `Knowledge_Base/Tasks/created_tasks.json` | Tareas en Google Tasks |
| `Knowledge_Base/Reminders/created_events.json` | Eventos en Google Calendar |

## Por qué source + title y no solo title

"Revisar el contrato" puede aparecer en múltiples contextos diferentes. Si se usara solo el título como clave, audios diferentes sobre el mismo tema se considerarían duplicados aunque sean instancias distintas.

Usar `source:title` asegura que solo se deduplica si es exactamente el mismo audio generando la misma tarea.

## Conceptos relacionados

- [[17_google_tasks_api]] — donde se usan los hashes para Tasks
- [[18_google_calendar_api]] — donde se usan los hashes para Calendar
- [[25_knowledge_base]] — los archivos JSON viven dentro de la KB
