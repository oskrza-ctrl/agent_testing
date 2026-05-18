# CONTEXT.md — Second Brain Agent

Archivo de contexto para retomar el proyecto en sesiones nuevas.

---

## Qué es

Sistema personal de captura y organización del conocimiento. Procesa audios de voz, los transcribe, clasifica el contenido en 6 categorías y lo organiza automáticamente en una Knowledge Base en Markdown. Tiene integraciones con Google Tasks, Calendar y Drive, un agente conversacional con búsqueda semántica (RAG), y un bot de Telegram como interfaz principal.

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

---

## Estructura del proyecto

```
agents/               ← 9 agentes especializados
core/
  message_handler.py  ← process_message() canal-agnóstico (NÚCLEO)
  agent_factory.py    ← build_message_handler() — inicializa todo
pipeline/             ← LangGraph (graph.py, nodes.py, state.py)
services/
  rag/                ← ChromaDB, indexer, intent_classifier (QUERY/CAPTURE/PIPELINE)
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
```

---

## Entrypoints

```bash
python main.py           # procesa todos los MP3 de input/
python chat.py           # chat en terminal (QUERY / CAPTURE / PIPELINE)
python telegram_bot.py   # bot de Telegram activo
```

---

## Flujo principal

```
[Audio MP3 o texto o voz Telegram]
        ↓
classify_intent → QUERY | CAPTURE | PIPELINE
        ↓
QUERY   → ChromaDB similarity search → GPT-4o-mini → respuesta semántica
CAPTURE → AnalysisAgent → KnowledgeBaseAgent → Tasks/Calendar → re-index
PIPELINE→ corre main.py → procesa MP3s del inbox → respuesta conversacional con GPT
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
| process_message() canal-agnóstico | CLI, Telegram y futura app usan la misma lógica |
| download_kb() en DriveAgent | Descarga KB de Drive antes de procesar para no sobreescribir archivos acumulativos |

---

## Estado actual

### ✅ Completado (pasos 0–20)
- Pipeline completo: MP3 → transcripción → análisis → Knowledge Base
- Google Tasks, Calendar, Drive (opcionales)
- LangGraph StateGraph con manejo de errores
- RAG conversacional con ChromaDB (QUERY + CAPTURE + PIPELINE)
- Bot de Telegram con voz, texto y comando /procesar
- MessageHandler canal-agnóstico + agent_factory
- Documentación: roadmap, decisions log (30 decisiones), first_agent_knowledge/ (bóveda Obsidian 35 notas), site/presentacion.html, site/architecture.html

### ⏳ Pendiente
- **Paso 21 — App propia (nuevo proyecto)**: dashboard web con chat IA + vistas de ideas/tareas/calendario/reuniones. Backend FastAPI reutilizando `core/`. Proyecto separado.
- **Despliegue 24/7 del bot**: el bot actualmente requiere que la PC esté encendida. Opciones evaluadas: Railway.app, Google Compute Engine e2-micro (free tier), webhook + Cloud Run Service. **No decidido aún.**
- **Cloud Run para main.py (paso 17)**: infraestructura lista en Google Cloud (proyecto second-brain-agent-496418, secrets en Secret Manager), pero el Job fue cancelado. Se retoma cuando se decida la estrategia de despliegue.

### Google Cloud — estado actual
- **Proyecto**: `second-brain-agent-496418`
- **APIs habilitadas**: Cloud Run, Cloud Scheduler, Secret Manager, Cloud Build
- **Secrets en Secret Manager**: OPENAI_API_KEY, GOOGLE_CREDENTIALS, GOOGLE_TOKEN_TASKS, GOOGLE_TOKEN_CALENDAR, GOOGLE_TOKEN_DRIVE
- **Container image**: `gcr.io/second-brain-agent-496418/second-brain-agent` (existe, está desactualizada)
- **Cloud Run Job**: eliminado (se canceló el enfoque de Job automático)

---

## Próxima decisión pendiente

Elegir dónde desplegar el bot de Telegram para que corra 24/7 sin la laptop:
1. **Railway.app** — más simple, free tier, 15 min de setup
2. **Google Compute Engine e2-micro** — free tier permanente, ya tienen Google Cloud
3. **Webhook + Cloud Run Service** — más complejo, paga por request
