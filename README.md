# Second Brain Agent

Sistema personal de captura y organización del conocimiento. Procesa audios de voz, los transcribe, clasifica el contenido automáticamente y lo organiza en una Knowledge Base en Markdown — con integraciones a Google Tasks, Google Calendar, Google Drive, un agente conversacional consultable desde Telegram, y una API HTTP para consumir desde cualquier app.

---

## Qué hace

```
Audio MP3 / Nota de voz / Texto / Llamada HTTP
        ↓
Transcripción (Whisper-1)
        ↓
Clasificación en 6 categorías (GPT-4o-mini)
        ↓
Knowledge Base Markdown  ←→  Google Tasks
                         ←→  Google Calendar
                         ←→  Google Drive
        ↓
Consulta semántica (RAG + ChromaDB)
        ↓
Chat conversacional: terminal · Telegram · API HTTP
```

**6 categorías de contenido:** Idea · Tarea · Recordatorio · Reunión · Proyecto · Nota general

**4 intenciones del agente:** QUERY · CAPTURE · PIPELINE · ACTION

---

## Entrypoints

| Comando | Para qué |
|---------|----------|
| `python main.py` | Procesa todos los MP3 de `input/` |
| `python chat.py` | Chat en terminal (consulta + captura + acciones) |
| `python telegram_bot.py` | Bot de Telegram (voz + texto desde el teléfono) |
| `python api.py` | API HTTP en `localhost:8000` |

---

## Despliegue (Railway.app)

Dos servicios corriendo 24/7 desde el mismo repo:

| Servicio | Start Command | URL |
|--|--|--|
| `agent_testing` | `python telegram_bot.py` | — (bot polling) |
| `agent-api` | `python api.py` | `https://<tu-dominio>.up.railway.app` |

Cada `git push origin main` redespliega ambos servicios automáticamente.

---

## API — endpoints principales

```
GET  /health              → estado del servicio
POST /chat                → {"message": "..."} → {"response": "..."}
GET  /kb/{category}       → contenido de la Knowledge Base
```

Categorías: `ideas · tasks · meetings · reminders · projects · notes`

Ver [`CONTEXT_API.md`](CONTEXT_API.md) para documentación completa con ejemplos.

---

## Estructura del proyecto

```
agent_testing/
├── main.py                  # Pipeline de procesamiento de MP3
├── chat.py                  # Chat conversacional en terminal
├── telegram_bot.py          # Bot de Telegram
├── api.py                   # API HTTP (FastAPI)
├── Procfile                 # Railway: worker + web
│
├── core/
│   ├── message_handler.py   # Lógica central canal-agnóstica
│   └── agent_factory.py     # Factory que inicializa todos los agentes
│
├── agents/                  # Agentes del pipeline
│   ├── transcription_agent.py
│   ├── analysis_agent.py
│   ├── markdown_agent.py
│   ├── knowledge_base_agent.py
│   ├── tasks_agent.py       # + find_and_complete()
│   ├── calendar_agent.py    # + archive_past_events()
│   ├── archive_agent.py
│   ├── drive_agent.py       # + download_kb()
│   └── query_agent.py       # Agente conversacional RAG
│
├── pipeline/                # LangGraph (StateGraph 9 nodos)
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
│
├── services/
│   ├── transcription/       # OpenAI Whisper
│   ├── analysis/            # OpenAI GPT-4o-mini
│   ├── tasks/               # Google Tasks API
│   ├── calendar/            # Google Calendar API
│   ├── drive/               # Google Drive API
│   └── rag/                 # ChromaDB + intent_classifier + action_classifier
│
├── prompts/                 # Prompts en Markdown
├── Knowledge_Base/          # Salida organizada
│   ├── Ideas/
│   ├── Tasks/
│   ├── Meetings/
│   ├── Reminders/
│   ├── Projects/
│   └── General_Notes/
│
├── input/                   # MP3 pendientes de procesar
├── processed/               # MP3 procesados
├── output/                  # Respaldos Markdown
├── chroma_db/               # Vector store local (gitignored)
├── temp/                    # Archivos temporales Telegram (gitignored)
├── credentials/             # Credenciales Google (gitignored)
│
├── docs/                    # Documentación técnica
├── site/                    # Presentación y arquitectura visual
└── first_agent_knowledge/   # Bóveda Obsidian con 35 notas del proyecto
```

---

## Setup local

### 1. Instalar dependencias

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
copy .env.example .env
```

Edita `.env` y agrega como mínimo:

```
OPENAI_API_KEY=sk-proj-...
```

### 3. Integraciones opcionales de Google

Para Tasks, Calendar y Drive:
1. Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com)
2. Habilitar las APIs: Tasks, Calendar, Drive
3. Crear credenciales OAuth 2.0 → descargar como `credentials/credentials.json`
4. Agregar tu email como usuario de prueba
5. Configurar los IDs de carpetas de Drive en `.env`

### 4. Bot de Telegram (opcional)

1. Habla con **@BotFather** en Telegram → `/newbot`
2. Agrega el token a `.env`:
   ```
   TELEGRAM_BOT_TOKEN=tu_token
   TELEGRAM_ALLOWED_USER_ID=tu_id_de_telegram
   ```

---

## Uso

### Chat en terminal

```bash
python chat.py
```

| Ejemplo | Intención |
|--|--|
| `¿qué ideas tengo del proyecto X?` | QUERY — búsqueda semántica |
| `idea: automatizar el reporte semanal` | CAPTURE — guarda en KB |
| `marca como completada la tarea de llamar a Juan` | ACTION — completa en Google Tasks |
| `archiva los eventos pasados` | ACTION — borra eventos pasados del calendario |
| `procesa los audios` | PIPELINE — procesa MP3s del inbox |

### API HTTP

```bash
python api.py
# Disponible en http://localhost:8000
# Docs interactivas: http://localhost:8000/docs
```

---

## Stack

| Componente | Tecnología |
|------------|-----------|
| Lenguaje | Python 3.11+ |
| Transcripción | OpenAI Whisper-1 |
| Análisis | OpenAI GPT-4o-mini |
| Orquestación | LangGraph (StateGraph) |
| Vector store | ChromaDB |
| Embeddings | OpenAI text-embedding-3-small |
| Tareas | Google Tasks API |
| Calendario | Google Calendar API |
| Almacenamiento | Google Drive API |
| Bot | python-telegram-bot |
| API | FastAPI + uvicorn |
| Despliegue | Railway.app |

---

## Documentación

- [`CONTEXT.md`](CONTEXT.md) — contexto completo para retomar el proyecto
- [`CONTEXT_API.md`](CONTEXT_API.md) — guía técnica para construir el frontend
- [`docs/roadmap_second_brain_agent.md`](docs/roadmap_second_brain_agent.md) — fases del proyecto
- [`docs/decisions_log.md`](docs/decisions_log.md) — registro de decisiones técnicas
- [`site/index.html`](site/index.html) — roadmap visual interactivo
- [`site/architecture.html`](site/architecture.html) — diagrama de arquitectura
- [`site/presentacion.html`](site/presentacion.html) — presentación de 21 slides
- [`first_agent_knowledge/`](first_agent_knowledge/) — bóveda Obsidian con 35 notas
