# Roadmap del Proyecto: Second Brain Agent

## Estado general

Este proyecto busca construir un sistema personal tipo “segundo cerebro” capaz de procesar audios, notas y textos para organizarlos automáticamente como ideas, tareas, reuniones, recordatorios, proyectos y notas generales.

El desarrollo se hará por fases, comenzando con un MVP local y evolucionando hacia un sistema automático en la nube con agentes, Google Drive, Google Tasks, Google Calendar y eventualmente un agente consultable.

---

# Roadmap

## 0. Preparación inicial

**Objetivo:** preparar el ambiente básico de trabajo.

**Estado:** Completado.

Actividades realizadas:

- Crear repositorio `agent_testing` en GitHub.
- Clonar el repositorio en la PC.
- Abrir el proyecto en VS Code.
- Configurar Claude Code.
- Crear archivo `CLAUDE.md` con instrucciones base del proyecto.

---

## 1. Estructura base del proyecto

**Objetivo:** crear la estructura inicial de carpetas y archivos.

**Estado:** Completado.

Estructura inicial:

```text
agent_testing/
├── input/
├── output/
├── services/
├── prompts/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── CLAUDE.md
```

---

## 2. Configuración de API

**Objetivo:** conectar el proyecto con OpenAI de forma segura.

**Estado:** Completado.

Actividades realizadas:

- Crear API key de OpenAI.
- Crear archivo `.env`.
- Leer `OPENAI_API_KEY` desde Python.
- Evitar subir `.env` a GitHub.
- Validar que la API key se carga correctamente.

---

## 3. MVP técnico básico

**Objetivo:** validar que el proceso principal funciona de inicio a fin.

**Estado:** Completado.

Flujo validado:

```text
MP3 en input/
↓
Transcripción con OpenAI
↓
Transcript guardado en output/
↓
Análisis con OpenAI
↓
Markdown generado en output/
```

Resultado esperado:

- Archivo `.txt` con transcript.
- Archivo `.md` con análisis del contenido.

---

## 4. Documentación del proyecto

**Objetivo:** documentar visión, alcance, decisiones y roadmap para evitar improvisar durante el desarrollo.

**Estado:** Completado.

Documentos creados:

```text
docs/
├── product_spec.md
├── technical_spec.md
├── roadmap.md
└── decisions_log.md
```

Decisiones funcionales documentadas:

- Ideas → archivo acumulativo `ideas.md`.
- Tareas → `tasks.md` + Google Tasks.
- Fecha sin hora → Google Tasks.
- Fecha con hora → Google Calendar.
- Información ambigua → Markdown como “requiere revisión”.
- Reuniones → archivo Markdown individual.
- Proyectos → archivo maestro `projects.md`.

---

## 5. Refactor a servicios

**Objetivo:** separar la lógica para evitar que todo viva en `main.py`.

**Estado:** Completado.

Servicios creados:

```text
services/
├── file_service.py
├── transcription_service.py
├── analysis_service.py
└── markdown_service.py
```

Responsabilidades:

- `file_service.py`: manejo de archivos de entrada y salida.
- `transcription_service.py`: transcripción de audio.
- `analysis_service.py`: análisis del transcript.
- `markdown_service.py`: generación y guardado de Markdown.
- `main.py`: punto de entrada simple.

---

## 6. Servicios intercambiables

**Objetivo:** preparar el proyecto para cambiar proveedores sin reescribir todo el flujo.

**Estado:** Completado.

Diseño esperado:

```text
Transcripción:
- OpenAI actualmente
- Whisper local en el futuro

Análisis de texto:
- OpenAI actualmente
- Modelo local en el futuro
```

Arquitectura preparada para:

```text
OpenAITranscriptionService
LocalWhisperTranscriptionService

OpenAIAnalysisService
LocalModelAnalysisService
```

---

## 7. Primera arquitectura tipo agentes

**Objetivo:** iniciar la transición hacia una arquitectura basada en agentes.

**Estado:** Completado.

Agentes creados:

```text
agents/
├── orchestrator_agent.py
├── transcription_agent.py
├── analysis_agent.py
├── markdown_agent.py
└── archive_agent.py
```

Estado actual:

- Los agentes existen como capas simples.
- Todavía no tienen prompts propios.
- Todavía no tienen comportamiento inteligente avanzado.
- Funcionan principalmente como wrappers organizados sobre servicios.

Flujo actual:

```text
main.py
↓
OrchestratorAgent
↓
TranscriptionAgent
↓
AnalysisAgent
↓
MarkdownAgent
↓
output/
```

---

# Próximas fases

## 8. Implementar Archive Agent

**Objetivo:** mover el MP3 procesado a una carpeta de archivos procesados.

**Estado:** Completado.

Implementado en `agents/archive_agent.py`:

- Crea `processed/` si no existe.
- Mueve el MP3 solo si todos los pasos anteriores fueron exitosos.
- Si ya existe un archivo con el mismo nombre, agrega timestamp para evitar sobreescribir.
- Integrado en `OrchestratorAgent` como último paso del pipeline.

---

## 9. Mejorar CLAUDE.md

**Objetivo:** definir reglas permanentes de trabajo para Claude Code.

**Estado:** Completado.

`CLAUDE.md` contiene sección de Coding Guidelines con:

- Código simple, claro y sin sobre-ingeniería.
- Comentarios breves donde ayuden a entender la intención.
- No implementar múltiples cambios grandes en una sola iteración.
- Explicar el plan antes de modificar código.
- Resumir cambios después de modificar código.
- No cambiar comportamiento existente sin avisar.

---

## 10. Agentes con prompts propios

**Objetivo:** convertir los agentes simples en agentes con instrucciones, reglas y criterios propios.

**Estado:** Completado.

Archivos creados en `prompts/`:

```text
prompts/
├── orchestrator_agent.md
├── analysis_agent.md
├── transcription_agent.md
├── markdown_agent.md
└── archive_agent.md
```

El `AnalysisAgent` carga `analysis_agent.md` al inicializarse via `services/prompt_loader.py`
y ensambla el prompt completo antes de enviarlo a OpenAI. El servicio recibe el prompt
ya armado y devuelve un `AnalysisResult` estructurado (JSON).

---

## 11. Clasificación real por tipo de contenido

**Objetivo:** clasificar cada entrada en una categoría principal y extraer elementos secundarios.

**Estado:** Completado.

Categorías implementadas:

```text
- Idea
- Reunión
- Tarea
- Recordatorio
- Proyecto
- Nota general
```

Estructura de datos: `services/analysis/analysis_result.py` define `AnalysisResult`
con los campos: `category`, `title`, `summary`, `ideas`, `tasks`, `reminders`,
`related_project`, `ambiguity_notes`, `tags`, `participants`, `decisions`,
`actions_for_me`, `actions_for_others`, `risks_blockers`, `next_steps`.

OpenAI responde con `response_format={“type”: “json_object”}` garantizando JSON válido.

Reglas aplicadas sobre fechas:

- Referencias relativas (“mañana”, “el viernes”) se preservan tal como se dijeron.
- Nunca se convierten en fechas absolutas inventadas.
- Se indica el candidato de destino: `[candidato: Google Calendar]` o `[candidato: Google Tasks]`.

---

## 11.5. Procesamiento múltiple de archivos

**Objetivo:** procesar todos los MP3 disponibles en `input/` en una sola ejecución.

**Estado:** Completado.

- `file_service.py`: `find_all_mp3()` devuelve lista ordenada de todos los MP3.
- `OrchestratorAgent.run()` itera sobre todos los archivos.
- `_process_one()` maneja el pipeline individual con `try/except` propio.
- Si un archivo falla, se muestra el error y se continúa con el siguiente.
- Al finalizar se imprime resumen: total encontrados, procesados OK y fallidos.

---

## 12. Salidas Markdown finales V1

**Objetivo:** escribir la información en una base de conocimiento organizada.

**Estado:** Completado.

Estructura implementada en `agents/knowledge_base_agent.py`:

```text
Knowledge_Base/
├── Ideas/
│   └── ideas.md          (acumulativo)
├── Tasks/
│   └── tasks.md           (acumulativo)
├── Meetings/
│   └── YYYY-MM-DD_titulo.md  (archivo individual por reunión)
├── Reminders/
│   └── reminders.md      (acumulativo)
├── Projects/
│   └── projects.md       (acumulativo)
└── General_Notes/
    └── YYYY-MM-DD_titulo.md  (archivo individual)
```

Reglas adicionales implementadas:

- Las tareas, recordatorios e ideas detectadas dentro de una Reunión o Nota general
  también se agregan a sus archivos acumulativos correspondientes (enrutado secundario).
- Los archivos de Reunión incluyen secciones enriquecidas: Participantes, Decisiones,
  Acciones para mí, Acciones para otros, Riesgos y bloqueos, Próximos pasos.
- Tags siempre presentes en toda salida (mínimo 2). Si no hay tags específicos,
  se usan tags de fallback: `#nota-general`, `#sin-proyecto`, `#requiere-revision`.
- El archivo `output/` sigue generándose como respaldo con el mismo contenido.

---

## 13. Integración con Google Tasks

**Objetivo:** crear tareas reales cuando el sistema detecte acciones pendientes.

**Estado:** Completado.

Implementado en `agents/tasks_agent.py` + `services/tasks/google_tasks_service.py`.

Reglas aplicadas:

| Caso | Acción |
|------|--------|
| Tarea clara sin fecha | Google Task con due date +7 días |
| Tarea clara con fecha pero sin hora | Google Task con due date |
| Recordatorio con fecha + hora | Reservado para Google Calendar |
| Ambiguo / “requiere revisión” | Solo Markdown |

Decisiones adicionales:
- El título incluye prefijo de proyecto: `[Proyecto] título de la tarea`.
- Deduplicación via `Knowledge_Base/Tasks/created_tasks.json` (hash por fuente + título).
- Lista dedicada en Google Tasks: **”Second Brain Agent”**.
- El sistema funciona aunque no haya credenciales (Google Tasks es opcional).

---

## 14. Integración con Google Calendar

**Objetivo:** crear eventos reales cuando el sistema detecte fecha y hora claras.

**Estado:** Completado.

Implementado en `agents/calendar_agent.py` + `services/calendar/google_calendar_service.py`.

Reglas aplicadas:

| Caso | Acción |
|------|--------|
| Recordatorio con fecha + hora | Evento en Google Calendar (1 hora de duración) |
| Recordatorio con solo fecha | Google Tasks (sin hora) |
| Ambiguo | Solo Markdown |

Decisiones adicionales:
- Título del evento: `result.title` (limpio y descriptivo, generado por el análisis).
- Duración por default: 1 hora.
- Timezone configurable via `.env` (`GOOGLE_CALENDAR_TIMEZONE`), default `America/Mexico_City`.
- Token separado de Google Tasks: `credentials/token_calendar.json`.
- Deduplicación via `Knowledge_Base/Reminders/created_events.json`.
- El sistema funciona aunque no haya credenciales (Google Calendar es opcional).

---

## 15. Integración con Google Drive

**Objetivo:** dejar de usar carpetas locales y procesar archivos desde Google Drive.

**Estado:** Completado.

Implementado en `services/drive/google_drive_service.py` + `agents/drive_agent.py`.

Flujo implementado:

```text
Drive/Second_Brain/Inbox/audio.mp3
    ↓ (DriveAgent.download_inbox)
input/audio.mp3
    ↓ (pipeline completo sin cambios)
Knowledge_Base/** + output/**
    ↓ (DriveAgent.upload_kb_file)
Drive/Second_Brain/Knowledge_Base/**
    ↓ (DriveAgent.move_to_processed)
Drive/Second_Brain/Processed/audio.mp3
```

Decisiones de diseño:

- Drive es una capa de I/O opcional — el pipeline principal no cambia.
- Si no hay carpetas configuradas en `.env`, el sistema usa carpetas locales.
- Los IDs de carpetas se configuran via `GOOGLE_DRIVE_INBOX_FOLDER_ID`,
  `GOOGLE_DRIVE_PROCESSED_FOLDER_ID` y `GOOGLE_DRIVE_KB_FOLDER_ID`.
- Los archivos KB se suben después de cada procesamiento individual.
- Al subir un archivo que ya existe en Drive, se actualiza en lugar de duplicar.
- Token separado de Tasks y Calendar: `credentials/token_drive.json`.
- Verificado en prueba real: 2 MP3 descargados, procesados, KB subida,
  archivos movidos a Processed en Drive.

---

## 16. Migración a LangGraph

**Objetivo:** convertir el flujo de agentes simples en un grafo formal de ejecución.

**Estado:** Completado.

Implementado en `pipeline/graph.py`, `pipeline/nodes.py`, `pipeline/state.py`.

Grafo implementado:

```text
transcription_node
↓
analysis_node
↓
markdown_node
↓
knowledge_base_node
↓
drive_sync_node (opcional)
↓
tasks_node (opcional)
↓
calendar_node (opcional)
↓
archive_node
↓
drive_processed_node (opcional)
↓
END
```

Diseño:

- `PipelineState` es el estado compartido que fluye entre nodos.
- Cada nodo envuelve un agente existente — los agentes no cambiaron.
- Si un nodo setea `error` en el estado, los nodos siguientes hacen early return.
- El MP3 no se mueve si ocurre error en cualquier nodo.
- Nodos opcionales (Drive, Tasks, Calendar) verifican si el agente existe antes de ejecutar.
- `OrchestratorAgent._process_one()` ahora invoca `pipeline.invoke(initial_state)`.
- Verificado en prueba real: pipeline completo con LangGraph, resultado idéntico al anterior.

---

## 17. Cloud Run + Cloud Scheduler

**Objetivo:** ejecutar el sistema automáticamente sin depender de la PC.

**Estado:** Pausado — se retoma después del paso 20.

Arquitectura esperada:

```text
Cloud Scheduler
↓
Cloud Run
↓
Google Drive
↓
OpenAI / modelos configurados
↓
Knowledge Base
```

---

## 18. Agente consultable RAG

**Objetivo:** chat conversacional con búsqueda semántica en la Knowledge Base y captura de contenido por texto.

**Estado:** Completado.

Implementado en `chat.py` + `services/rag/` + `agents/query_agent.py`.

Arquitectura:

```text
python chat.py
↓
Indexa Knowledge_Base/ en ChromaDB (text-embedding-3-small)
↓
Loop conversacional:
  classify_intent(GPT-4o-mini) → QUERY | CAPTURE
  QUERY   → QueryAgent → ChromaDB similarity search → GPT-4o-mini → respuesta
  CAPTURE → AnalysisAgent → KnowledgeBaseAgent + TasksAgent + CalendarAgent → re-indexado
```

Componentes creados:

```text
services/rag/
├── base.py                  (interfaz RAGService)
├── indexer.py               (chunkea KB por separador ---)
├── chromadb_rag_service.py  (ChromaDB + embeddings + GPT)
└── intent_classifier.py     (QUERY vs CAPTURE via GPT)

agents/query_agent.py        (historial de conversación, MAX_HISTORY=10)
prompts/query_agent.md       (instrucciones: no alucinar, citar fuente)
chat.py                      (entrypoint, loop, comandos reset/salir)
```

Decisiones:
- ChromaDB local persistente en `chroma_db/` (gitignored)
- Re-indexado completo al arrancar y tras cada CAPTURE (< 2 segundos)
- Modo CAPTURE en chat crea .md en `output/` y en `Knowledge_Base/` igual que los audios

---

## 19. Refactor MessageHandler

**Objetivo:** extraer la lógica conversacional a un núcleo reutilizable por cualquier canal.

**Estado:** Completado.

Componentes creados:

```text
core/
├── message_handler.py   ← MessageHandler con process_message() y process_voice()
└── agent_factory.py     ← build_message_handler() — inicializa todos los agentes
```

`chat.py` quedó reducido a ~40 líneas — solo el loop de terminal.
Cualquier canal nuevo solo llama `handler.process_message(text)`.

---

## 20. Telegram — canal completo

**Objetivo:** usar Telegram como canal de captura y consulta desde el teléfono.

**Estado:** Completado.

Implementado en `telegram_bot.py`.

Flujo implementado:

```text
[Nota de voz] → descarga .ogg → Whisper → AnalysisAgent → KB + Tasks + Calendar → respuesta
[Texto]       → classify_intent (GPT) → QUERY o CAPTURE → respuesta
[/start]      → bienvenida
[/reset]      → reinicia historial de conversación
```

Decisiones:
- Modo polling (no requiere URL pública — suficiente para uso personal local)
- Whitelist via `TELEGRAM_ALLOWED_USER_ID` en `.env`
- Audios de voz siempre son CAPTURE (no pasan por clasificador de intención)
- Indicador "escribiendo..." mientras procesa para mejor UX

---

## 21. App propia — dashboard central (FUTURO — nuevo proyecto)

**Objetivo:** app con chat IA + vistas de ideas, tareas, calendario y resúmenes de reuniones.

**Estado:** Futuro — será un proyecto separado.

Componentes esperados:
- Backend FastAPI reutilizando `core/message_handler.py`
- Dashboard web: lista de ideas, tareas, resúmenes de reuniones, calendario
- Chat IA embebido
- La misma `core/` del agente actual como librería base

---

# Resumen visual

```text
✅ Preparación inicial
✅ Estructura base
✅ API key y configuración
✅ MVP técnico MP3 → transcript → Markdown
✅ Documentación
✅ Servicios modulares
✅ Servicios intercambiables
✅ Primeros agentes simples
✅ Archive Agent (MP3 → processed/)
✅ CLAUDE.md mejorado
✅ Prompts propios para agentes
✅ Clasificación real por tipo (6 categorías + JSON estructurado)
✅ Procesamiento múltiple de archivos
✅ Knowledge Base Markdown V1
✅ Google Tasks (tareas con due date, prefijo de proyecto, deduplicación)
✅ Google Calendar (eventos con fecha + hora, deduplicación)
✅ Google Drive (Inbox → proceso local → KB en Drive → Processed)
✅ LangGraph (StateGraph con 9 nodos, estado compartido, manejo de errores formal)
✅ Agente consultable RAG (ChromaDB + embeddings + chat dual QUERY/CAPTURE)
✅ MessageHandler — process_message() canal-agnóstico
✅ Telegram Bot (polling, voz + texto, whitelist de seguridad)

➡️ Cloud Run + Scheduler (paso 17 — siguiente cuando se quiera desplegar)
🚀 App propia dashboard (paso 21 — nuevo proyecto futuro)
```

---

# Estado final del proyecto

El sistema está completo como herramienta personal de segundo cerebro:

```text
[Audios MP3 en PC]          → python main.py       → KB + Tasks + Calendar
[Texto o voz en Telegram]   → python telegram_bot.py → KB + Tasks + Calendar
[Consultas en terminal]     → python chat.py        → respuesta semántica
[Consultas en Telegram]     → bot activo            → respuesta semántica
```

Todo converge en la misma `Knowledge_Base/` local, sincronizable a Google Drive.
La arquitectura está lista para conectarse a una app web (paso 21) o desplegarse en la nube (paso 17).
