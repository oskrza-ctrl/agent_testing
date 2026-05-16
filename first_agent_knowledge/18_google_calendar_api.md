---
tags: [google, calendar, api, eventos, integracion]
---

# Google Calendar API

Google Calendar API permite crear eventos de calendario desde código. El proyecto la usa cuando el análisis detecta un recordatorio con fecha **y** hora explícitas.

## Crear un evento

```python
from googleapiclient.discovery import build

service = build("calendar", "v3", credentials=creds)

event_body = {
    "summary": "Revisión contrato BOYA",     # título del evento
    "start": {
        "dateTime": "2026-05-20T10:00:00",
        "timeZone": "America/Mexico_City",
    },
    "end": {
        "dateTime": "2026-05-20T11:00:00",   # duración: 1 hora (default)
        "timeZone": "America/Mexico_City",
    },
}

event = service.events().insert(
    calendarId="primary",   # calendario principal del usuario
    body=event_body
).execute()
```

## Scopes requeridos

```python
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
# Solo permisos para events — no para leer toda la configuración del calendario
```

Token guardado en `credentials/token_calendar.json` (separado de Tasks).

## Reglas de creación de eventos

| Condición | Acción |
|-----------|--------|
| Recordatorio con fecha + hora | Evento en Google Calendar |
| Recordatorio con solo fecha | Google Tasks (sin hora) |
| Recordatorio ambiguo | Solo Markdown |

El marcador `[candidato: Google Calendar]` en el texto del recordatorio indica que el análisis encontró fecha y hora.

## Título del evento: result.title, no el texto crudo

Un error inicial: se usaba el texto crudo del recordatorio como título, lo que generaba títulos como "Llamar al cliente mañana a las 10am [candidato: Google Calendar]".

La solución: usar `result.title` (generado por el agente de análisis), que es siempre limpio y descriptivo.

```python
event_body = {
    "summary": result.title,   # "Llamada con cliente BOYA"
    ...
}
```

## Timezone configurable

```python
timezone = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "America/Mexico_City")
```

Se puede cambiar en `.env` sin tocar el código.

## Conceptos relacionados

- [[27_reglas_calendario_tareas]] — lógica de cuándo crear event vs task
- [[26_deduplicacion]] — evitar duplicar el mismo evento
- [[16_google_oauth2]] — autenticación para la API
- [[17_google_tasks_api]] — su equivalente para tareas
