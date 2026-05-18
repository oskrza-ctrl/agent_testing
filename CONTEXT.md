# CONTEXT.md — Second Brain Agent

Archivo de contexto para retomar el proyecto en sesiones nuevas.

---

## Qué es

Sistema personal de captura y organización del conocimiento. Procesa audios de voz, los transcribe, clasifica el contenido en 6 categorías y lo organiza automáticamente en una Knowledge Base en Markdown. Tiene integraciones con Google Tasks, Calendar y Drive, un agente conversacional con búsqueda semántica (RAG), un bot de Telegram como interfaz principal, y una API HTTP para consumir desde cualquier app.

---

## Stack

| Componente | Tecnología |
|--|--|
| Lenguaje | Python 3.11+ |
| Transcripción | OpenAI Whisper-1 (~$0.006/min) |
| Análisis / Chat | OpenAI GPT-4o-mini (~$0.15/M tokens) |
| Embeddings | OpenAI text-embedding-3-small |
| Orquestación | LangGraph StateGraph (9 nodos) |
| Vector store | ChromaDB (local, persistente) |
| Google Tasks | google-api-python-client |
| Google Calendar | google-api-python-client |
| Google Drive | google-api-python-client |
| Bot | python-telegram-bot (polling) |
| API HTTP | FastAPI + uvicorn |
| Despliegue | Railway.app (2 servicios) |

---

## Estructura del proyecto

```
agents/               ← 9 agentes especializados
core/
  message_handler.py  ← process_message() canal-agnóstico (NÚCLEO)
  agent_factory.py    ← build_message_handler() — inicializa todo
pipeline/             ← LangGraph (graph.py, nodes.py, state.py)
services/
  rag/                ← ChromaDB, indexer, intent_classifier, action_classifier
  transcription/      ← OpenAI Whisper
  analysis/           ← OpenAI GPT-4o-mini + AnalysisResult dataclass
  tasks/              ← Google Tasks API
  calendar/           ← Google Calendar API
  drive/              ← Google Drive API
prompts/              ← prompts en Markdown (analysis_agent.md, query_agent.md)
Knowledge_Base/       ← salida organizada (Ideas, Tasks, Meetings, Reminders, Projects, Notes)
chroma_db/            ← vector store local (gitignored)
credentials/          ← OAuth tokens Google (gitignored)
main.py               ← procesa MP3s de input/
chat.py               ← chat conversacional en terminal
telegram_bot.py       ← bot de Telegram
api.py                ← API HTTP (FastAPI)
Procfile              ← Railway: worker=telegram_bot.py, web=api.py
```

---

## Entrypoints

```bash
python main.py           # procesa todos los MP3 de input/
python chat.py           # chat en terminal (QUERY / CAPTURE / PIPELINE / ACTION)
python telegram_bot.py   # bot de Telegram activo
python api.py            # API HTTP en localhost:8000
```

---

## Flujo principal — clasificador de dos niveles

```
[Audio MP3 o texto o voz Telegram o llamada HTTP]
        ↓
Level 1: classify_intent → QUERY | CAPTURE | PIPELINE | ACTION
        ↓
QUERY    → ChromaDB similarity search → GPT-4o-mini → respuesta semántica
CAPTURE  → AnalysisAgent → KnowledgeBaseAgent → Tasks/Calendar → re-index
PIPELINE → corre main.py → procesa MP3s del inbox → resumen conversacional
ACTION   → Level 2: classify_action → COMPLETE_TASK | ARCHIVE_EVENTS
                    COMPLETE_TASK  → lista tareas → GPT elige → complete_task()
                    ARCHIVE_EVENTS → lista eventos pasados → delete_event()
```

---

## LangGraph pipeline (9 nodos)

```
transcription → analysis → markdown → knowledge_base →
drive_sync → tasks → calendar → archive → drive_processed → END
```

- Error en cualquier nodo → `state["error"]` → early return → MP3 no se mueve
- Nodos 5,6,7,9 son opcionales (requieren credenciales Google)

---

## AnalysisResult — objeto central

15 campos: `category, title, summary, ideas[], tasks[], reminders[], related_project, ambiguity_notes, tags[], participants[], decisions[], actions_for_me[], actions_for_others[], risks_blockers[], next_steps[]`

6 categorías: `Idea | Tarea | Recordatorio | Reunión | Proyecto | Nota general`

---

## Knowledge Base routing

- **ACCUMULATIVE** (un archivo): Ideas/ideas.md, Tasks/tasks.md, Reminders/reminders.md, Projects/projects.md
- **INDIVIDUAL** (un archivo por entrada): Meetings/YYYY-MM-DD_title.md, General_Notes/YYYY-MM-DD_title.md
- **Secondary routing**: tasks/ideas/reminders dentro de Reuniones también van a sus archivos acumulativos

---

## API HTTP — endpoints

```
GET  /health              → {"status": "ok"}
POST /chat                → {"message": "..."} → {"response": "..."}
GET  /kb/{category}       → contenido de la KB
```

Categorías válidas: `ideas | tasks | meetings | reminders | projects | notes`

Acumulativas devuelven `{category, content}`.
Individuales (meetings, notes) devuelven `{category, files: [{name, content}]}`.

Sin autenticación por ahora — pendiente agregar API Key.

---

## Variables de entorno (.env)

```
OPENAI_API_KEY=sk-proj-...
TELEGRAM_BOT_TOKEN=...
TELEGRAM_ALLOWED_USER_ID=1043931661
GOOGLE_CREDENTIALS_FILE=credentials/credentials.json
GOOGLE_TOKEN_FILE=credentials/token.json
GOOGLE_CALENDAR_TOKEN_FILE=credentials/token_calendar.json
GOOGLE_DRIVE_TOKEN_FILE=credentials/token_drive.json
GOOGLE_DRIVE_INBOX_FOLDER_ID=1pgehcCoulbemk_c1XmF1WOMQ-iwYEWPz
GOOGLE_DRIVE_PROCESSED_FOLDER_ID=1a0xbNnV4R19Fv6LZjrWZnQOHW7BUh_c0
GOOGLE_DRIVE_KB_FOLDER_ID=1rtYFbFItvoZrI1V0xN018mLU-3uOoy9r
GOOGLE_CALENDAR_TIMEZONE=America/Mexico_City
```

En Railway se usan además:
```
GOOGLE_CREDENTIALS_B64=...       ← credentials.json en base64
GOOGLE_TOKEN_TASKS_B64=...       ← token.json en base64
GOOGLE_TOKEN_CALENDAR_B64=...    ← token_calendar.json en base64
GOOGLE_TOKEN_DRIVE_B64=...       ← token_drive.json en base64
```

---

## Despliegue — Railway.app

Dos servicios en el mismo proyecto Railway, mismo repo `oskrza-ctrl/agent_testing`:

| Servicio | Start Command | Tipo | Estado |
|--|--|--|--|
| `agent_testing` | `python telegram_bot.py` | worker | Online ✅ |
| `agent-api` | `python api.py` | web | Online ✅ |

El deploy se dispara automáticamente con cada `git push origin main`.

---

## Decisiones importantes

| Decisión | Razón |
|--|--|
| gpt-4o-mini sobre GPT-4o | 16× más barato, suficiente para clasificación |
| ChromaDB local | Gratuito, sin infraestructura externa |
| Servicios con abstract base classes | Proveedores intercambiables sin tocar el pipeline |
| Markdown primero | Compatible con Obsidian, versionable con git |
| Google integrations opcionales | Sistema funciona sin credenciales |
| Polling Telegram (no webhook) | No requiere URL pública para desarrollo local |
| Whitelist por TELEGRAM_ALLOWED_USER_ID | Seguridad — el bot solo responde al propietario |
| Re-index ChromaDB tras cada CAPTURE | Siempre fresco, < 2s, sin complejidad incremental |
| process_message() canal-agnóstico | CLI, Telegram y API usan la misma lógica |
| download_kb() en DriveAgent | Descarga KB de Drive antes de procesar para no sobreescribir archivos acumulativos |
| Credenciales Google en base64 (Railway) | Los archivos de credentials/ son gitignored; se reconstruyen al arrancar desde env vars |
| Dos servicios Railway (no uno) | Railway corre un proceso por servicio; worker+web requieren servicios separados |
| Clasificador de dos niveles (ACTION) | Level 1 detecta que es acción, Level 2 determina cuál — más robusto que un solo clasificador con muchas categorías |
| Sin auth en API por ahora | URL no es fácil de adivinar; se agrega API Key cuando empiece el frontend |

---

## Estado actual

### ✅ Completado

- Pipeline completo: MP3 → transcripción → análisis → Knowledge Base
- Google Tasks, Calendar, Drive (opcionales)
- LangGraph StateGraph con manejo de errores
- RAG conversacional con ChromaDB
- Clasificador de intención de dos niveles: QUERY / CAPTURE / PIPELINE / ACTION
- Acciones: marcar tareas como completadas, archivar eventos pasados
- Bot de Telegram con voz, texto y comando /procesar — corriendo 24/7 en Railway
- API HTTP (FastAPI) con /chat y /kb/{category} — corriendo en Railway
- Credenciales Google inyectadas via variables de entorno en Railway
- Documentación: roadmap, decisions log, Obsidian vault (35 notas), presentacion.html, architecture.html

### ⏳ Pendiente

- **Paso 21 — App frontend (nuevo proyecto)**: dashboard web que consume la API. Repo separado.
  Ver `CONTEXT_API.md` para toda la información técnica necesaria para ese proyecto.
- **Auth en la API**: agregar `X-API-Key` header una vez que empiece el frontend.
- **Persistencia en Railway**: chroma_db/ y Knowledge_Base/ son efímeros. Agregar Railway Volume si se necesita persistencia entre deploys.
