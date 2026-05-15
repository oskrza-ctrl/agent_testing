# Second Brain Agent - Roadmap

**Versión:** 0.1  
**Fecha:** 2026-05-14  
**Referencia:** `second_brain_agent_functional_spec.md` sección 16

---

## Estado actual

**Fase 0 completada:** Pipeline MVP local funcionando.

- MP3 en `input/` → transcripción → análisis → Markdown en `output/`
- API key cargada desde `.env`
- Transcripción con `whisper-1`
- Análisis con `gpt-4o-mini`

---

## V1 — Organización local completa

**Objetivo:** Convertir el pipeline en un sistema de conocimiento organizado, sin intervención manual.

### Fase 1 — Knowledge Base en Markdown

- [ ] Crear estructura de carpetas `Knowledge_Base/`
- [ ] Separar ideas en `ideas.md` (archivo acumulativo)
- [ ] Separar tareas en `tasks.md` (archivo acumulativo)
- [ ] Crear archivos individuales por reunión en `Meetings/`
- [ ] Crear archivo maestro de proyectos `projects.md`
- [ ] Guardar recordatorios en `reminders.md`
- [ ] Mover archivos procesados a `Processed/`
- [ ] Evitar procesar el mismo archivo dos veces

### Fase 2 — Servicios modulares

- [ ] Separar código de `main.py` en servicios independientes
- [ ] Crear `TranscriptionService` con interfaz intercambiable
- [ ] Crear `TextAnalysisService` con interfaz intercambiable
- [ ] Crear `FileService` para manejo de archivos
- [ ] Mover prompts a `prompts/`
- [ ] Soporte para entradas TXT y MD (además de MP3)

### Fase 3 — Google Tasks y Google Calendar

- [ ] Conectar Google Tasks API
- [ ] Crear tareas con fecha cuando aplique
- [ ] Conectar Google Calendar API
- [ ] Crear eventos solo cuando haya fecha y hora claras
- [ ] Marcar contenido ambiguo como "requiere revisión"

---

## V2 — Automatización y cloud

**Objetivo:** Eliminar la necesidad de ejecutar el script manualmente desde el PC local.

### Fase 4 — Google Drive

- [ ] Leer archivos desde `Second_Brain/Inbox/` en Google Drive
- [ ] Escribir Markdown de salida en Google Drive
- [ ] Mover archivos procesados en Google Drive

### Fase 5 — Cloud Run y Scheduler

- [ ] Contenerizar con Docker
- [ ] Desplegar en Google Cloud Run
- [ ] Programar ejecuciones periódicas con Cloud Scheduler
- [ ] Logs y monitoreo básico

---

## V3 — Agente consultable e integraciones conversacionales

**Objetivo:** Poder consultar el conocimiento acumulado mediante lenguaje natural.

### Fase 6 — Agentes y LangGraph

- [ ] Crear Orchestrator Agent
- [ ] Separar agentes por responsabilidad (intake, clasificación, escritura)
- [ ] Migrar pipeline a LangGraph
- [ ] Whisper local para transcripción sin costo
- [ ] Modelo local via Ollama para análisis sin costo por token

### Fase 7 — Agente consultable

- [ ] Indexar `Knowledge_Base/` para búsqueda semántica
- [ ] Responder preguntas sobre ideas, tareas, reuniones y proyectos
- [ ] Interfaz de consulta inicial (CLI o web simple)

### Fase 8 — Integraciones conversacionales (futuro)

- [ ] Chat web
- [ ] Telegram
- [ ] WhatsApp
- [ ] Slack
- [ ] App móvil

---

## Criterio de éxito por versión

| Versión | Éxito cuando... |
|---|---|
| V1 | El usuario coloca un MP3 y obtiene ideas, tareas, minutas y recordatorios organizados automáticamente |
| V2 | El sistema corre en la nube sin intervención del usuario y procesa archivos desde Google Drive |
| V3 | El usuario puede preguntar "¿qué pendientes tengo esta semana?" y obtener una respuesta basada en su Knowledge Base |
