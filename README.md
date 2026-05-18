# Second Brain Agent

Sistema personal de captura y organización del conocimiento. Procesa audios de voz, los transcribe, clasifica el contenido automáticamente y lo organiza en una Knowledge Base en Markdown — con integraciones a Google Tasks, Google Calendar, Google Drive y un agente conversacional consultable desde Telegram.

---

## Qué hace

```
Audio MP3 / Nota de voz / Texto
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
Chat conversacional: terminal o Telegram
```

**6 categorías de contenido:** Idea · Tarea · Recordatorio · Reunión · Proyecto · Nota general

---

## Entrypoints

| Comando | Para qué |
|---------|----------|
| `python main.py` | Procesa todos los MP3 de `input/` |
| `python chat.py` | Chat en terminal (consulta + captura por texto) |
| `python telegram_bot.py` | Bot de Telegram (voz + texto desde el teléfono) |

---

## Estructura del proyecto

```
agent_testing/
├── main.py                  # Pipeline de procesamiento de MP3
├── chat.py                  # Chat conversacional en terminal
├── telegram_bot.py          # Bot de Telegram
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
│   ├── tasks_agent.py
│   ├── calendar_agent.py
│   ├── archive_agent.py
│   ├── drive_agent.py
│   └── query_agent.py       # Agente conversacional RAG
│
├── pipeline/                # LangGraph (StateGraph 9 nodos)
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
│
├── services/                # Servicios intercambiables
│   ├── transcription/       # OpenAI Whisper
│   ├── analysis/            # OpenAI GPT-4o-mini
│   ├── tasks/               # Google Tasks API
│   ├── calendar/            # Google Calendar API
│   ├── drive/               # Google Drive API
│   └── rag/                 # ChromaDB + embeddings
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
├── site/                    # Roadmap visual (abrir index.html)
└── first_agent_knowledge/   # Bóveda Obsidian con documentación del proyecto
```

---

## Setup

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

Para Tasks, Calendar y Drive necesitas:
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
   Tu ID lo obtienes escribiéndole a **@userinfobot**.

---

## Uso

### Procesar audios

Coloca archivos `.mp3` en `input/` y ejecuta:

```bash
python main.py
```

El sistema transcribe, clasifica, organiza en la Knowledge Base y (si están configuradas) crea tareas en Google Tasks y eventos en Google Calendar.

### Chat en terminal

```bash
python chat.py
```

Escribe preguntas o captura contenido nuevo:
- `¿qué ideas tengo del proyecto X?` → búsqueda semántica en la KB
- `idea: automatizar el reporte semanal` → clasifica y guarda en la KB
- `reset` → nueva conversación
- `salir` → cerrar

### Bot de Telegram

```bash
python telegram_bot.py
```

Desde Telegram:
- Envía una nota de voz → se transcribe y guarda automáticamente
- Escribe un mensaje → el agente detecta si es pregunta o captura
- `/reset` → nueva conversación
- `/start` → instrucciones

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

---

## Documentación

- [`docs/roadmap_second_brain_agent.md`](docs/roadmap_second_brain_agent.md) — fases del proyecto
- [`docs/decisions_log.md`](docs/decisions_log.md) — registro de decisiones técnicas
- [`site/index.html`](site/index.html) — roadmap visual interactivo
- [`site/architecture.html`](site/architecture.html) — diagrama de arquitectura
- [`first_agent_knowledge/`](first_agent_knowledge/) — bóveda Obsidian con 35 notas explicando cada concepto del proyecto
