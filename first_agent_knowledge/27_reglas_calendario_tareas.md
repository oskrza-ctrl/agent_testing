---
tags: [reglas, calendario, tareas, enrutado, decision]
---

# Reglas: cuándo crear Task vs Event vs solo Markdown

El sistema tiene reglas precisas para decidir qué hacer con cada tarea y recordatorio detectado. Una mala asignación contamina el calendario con eventos en fechas incorrectas o llena Google Tasks con elementos que deberían estar en el calendario.

## Tabla de decisión

| Contenido detectado | Marcador | Acción |
|---------------------|----------|--------|
| Tarea clara sin fecha | — | Google Task con due date +7 días |
| Tarea con fecha relativa ("mañana") | — | Google Task con due date calculado |
| Tarea ambigua / "requiere revisión" | — | Solo Markdown, no se crea task |
| Recordatorio con fecha + hora | `[candidato: Google Calendar]` | Evento en Google Calendar |
| Recordatorio con solo fecha | `[candidato: Google Tasks]` | Google Task con due date |
| Recordatorio ambiguo | sin marcador | Solo Markdown |

## Los marcadores

El agente de análisis inyecta marcadores en el texto de los recordatorios:

```
"Reunión con el equipo el viernes a las 3pm [candidato: Google Calendar]"
"Revisar el informe el lunes [candidato: Google Tasks]"
"Pendiente de definir fecha [requiere revisión]"
```

El `TasksAgent` lee estos marcadores para decidir qué hacer:

```python
_CALENDAR_MARKER = "[candidato: google calendar]"
_TASKS_MARKER    = "[candidato: google tasks]"

for reminder_text in result.reminders:
    lower = reminder_text.lower()
    if _CALENDAR_MARKER in lower:
        continue   # CalendarAgent lo manejará
    if _TASKS_MARKER not in lower:
        continue   # ambiguo, solo Markdown
    # Crear Google Task
```

El `CalendarAgent` solo procesa recordatorios con `[candidato: Google Calendar]`.

## Por qué esta regla existe

Sin esta separación, el sistema podría:
- Crear eventos de calendario para "revisar algo algún día" (sin fecha)
- Crear tareas de Google Tasks para "reunión el martes a las 4pm" (que debería ser un evento)
- Duplicar el mismo elemento en Tasks Y Calendar

La regla mantiene cada herramienta para su propósito:
- **Google Tasks**: lista de pendientes, cosas que hacer
- **Google Calendar**: compromisos en fecha y hora específica

## Resolución de fechas relativas

```python
def _resolve_date(self, text: str) -> Optional[date]:
    today = date.today()
    lower = text.lower()

    if "mañana" in lower:
        return today + timedelta(days=1)
    if "pasado mañana" in lower:
        return today + timedelta(days=2)

    for day_name, weekday_idx in _DAYS.items():
        if day_name in lower:
            ahead = weekday_idx - today.weekday()
            if ahead <= 0:
                ahead += 7   # siguiente ocurrencia del día
            return today + timedelta(days=ahead)

    return today + timedelta(days=7)  # default: 7 días
```

## Conceptos relacionados

- [[17_google_tasks_api]] — implementación de creación de Tasks
- [[18_google_calendar_api]] — implementación de creación de Events
- [[24_categorias_contenido]] — la categoría "Recordatorio" y sus reglas
