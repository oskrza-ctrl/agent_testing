# Second Brain Agent - Especificación Técnica

**Versión:** 0.1  
**Fecha:** 2026-05-14  
**Estado:** En construcción

---

## 1. Stack actual

| Componente | Tecnología | Notas |
|---|---|---|
| Lenguaje | Python 3.x | |
| Transcripción | OpenAI `whisper-1` | Intercambiable por Whisper local en V1.5 |
| Análisis de texto | OpenAI `gpt-4o-mini` | Intercambiable por modelo local en V2 |
| Variables de entorno | `python-dotenv` | Lee desde `.env` |
| Gestión de rutas | `pathlib.Path` | Nativo de Python |
| Salida | Archivos Markdown y TXT | Sin base de datos en V1 |

---

## 2. Estructura de carpetas actual

```
agent_testing/
├── input/              # Archivos de entrada (MP3, TXT, MD)
├── output/             # Salida actual del pipeline (temporal)
├── services/           # Módulos de integración (vacío por ahora)
├── prompts/            # Prompts reutilizables (vacío por ahora)
├── docs/               # Documentación del proyecto
│   ├── second_brain_agent_functional_spec.md
│   ├── technical_spec.md
│   ├── roadmap.md
│   └── decisions_log.md
├── main.py             # Entry point del pipeline
├── requirements.txt    # Dependencias Python
├── .env.example        # Template de variables de entorno
├── .gitignore
├── CLAUDE.md
└── README.md
```

---

## 3. Estructura de carpetas objetivo (V1 completa)

```
agent_testing/
├── input/
├── Knowledge_Base/
│   ├── Ideas/
│   │   └── ideas.md
│   ├── Tasks/
│   │   └── tasks.md
│   ├── Meetings/
│   │   └── YYYY-MM-DD_titulo_reunion.md
│   ├── Reminders/
│   │   └── reminders.md
│   ├── Projects/
│   │   └── projects.md
│   ├── General_Notes/
│   │   └── YYYY-MM-DD_titulo_nota.md
│   ├── Transcripts/
│   │   └── archivo_original_transcript.txt
│   └── Processed/
│       └── (archivos ya procesados)
├── services/
│   ├── transcription_service.py
│   ├── analysis_service.py
│   ├── file_service.py
│   ├── task_service.py
│   └── calendar_service.py
├── prompts/
│   └── analysis_prompt.txt
├── docs/
└── main.py
```

---

## 4. Arquitectura del pipeline actual

```
input/archivo.mp3
    ↓
Detectar tipo de archivo
    ↓
Si MP3 → Transcribir con whisper-1
Si TXT/MD → Leer directamente
    ↓
Analizar con gpt-4o-mini
    ↓
Guardar transcript en output/
Guardar análisis Markdown en output/
```

---

## 5. Servicios planificados (diseño modular)

El código debe diseñarse con interfaces intercambiables para no depender permanentemente de un proveedor.

| Servicio | Implementación V1 | Implementación futura |
|---|---|---|
| `TranscriptionService` | `OpenAITranscriptionService` | `LocalWhisperTranscriptionService` |
| `TextAnalysisService` | `OpenAITextAnalysisService` | `LocalModelTextAnalysisService` (Ollama) |
| `FileService` | `MarkdownFileService` | Compatible con Google Drive |
| `TaskService` | Markdown local | `GoogleTasksService` |
| `CalendarService` | No aplica en V1 | `GoogleCalendarService` |

---

## 6. Decisiones técnicas

| Decisión | Elección | Razón |
|---|---|---|
| Modelo de transcripción | `whisper-1` | Más económico disponible en OpenAI API |
| Modelo de análisis | `gpt-4o-mini` | Económico y suficiente para análisis de texto |
| Sin base de datos | Markdown plano | Legible por humanos, compatible con Obsidian y Google Drive |
| Sin LangGraph en V1 | Pipeline secuencial | Validar flujo simple antes de complejizar |
| Servicios intercambiables | Interfaces modulares | Evitar lock-in con un proveedor |

---

## 7. Variables de entorno requeridas

```env
OPENAI_API_KEY=sk-...
```

Variables futuras:
```env
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json
GOOGLE_TASKS_LIST_ID=...
GOOGLE_CALENDAR_ID=...
```

---

## 8. Dependencias actuales

```
openai
python-dotenv
```

Dependencias futuras:
```
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
```
