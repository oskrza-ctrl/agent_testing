---
tags: [fastapi, railway, api, despliegue, uvicorn]
---

# FastAPI y despliegue en Railway

## FastAPI

Framework web moderno para crear APIs HTTP en Python. Ventajas clave:
- Validación automática con Pydantic
- Documentación interactiva autogenerada en `/docs`
- Async-ready, alto rendimiento
- Muy poco código para un endpoint funcional

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    response = handler.process_message(req.message)
    return {"response": response}
```

## Uvicorn

Servidor ASGI que corre la aplicación FastAPI. FastAPI define los endpoints; uvicorn los sirve:

```bash
python api.py          # arranca uvicorn internamente
# o directamente:
uvicorn api:app --host 0.0.0.0 --port 8000
```

## CORS

Permite que un frontend en otro dominio llame a la API. Sin CORS el navegador bloquea las peticiones:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # cualquier origen — restringir en producción
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Endpoints del proyecto

```
GET  /health              → {"status": "ok"}
POST /chat                → {"message": "..."} → {"response": "..."}
GET  /kb/{category}       → contenido de la Knowledge Base
```

Categorías de KB: `ideas · tasks · meetings · reminders · projects · notes`

## Railway.app

Plataforma de despliegue que conecta directamente con GitHub. Cada push a `main` redespliega automáticamente.

### Cómo funciona

1. Conectas tu repo de GitHub
2. Railway detecta el `Procfile` y sabe qué correr
3. Lee las variables de entorno que configuras en el panel
4. Asigna una URL pública al servicio web

### Procfile

Archivo en la raíz del repo que le dice a Railway qué procesos correr:

```
worker: python telegram_bot.py    ← proceso sin puerto HTTP
web: python api.py                ← proceso con puerto HTTP (Railway asigna PORT)
```

**Importante:** Railway corre UN proceso por servicio. Para tener `worker` + `web` simultáneamente necesitas DOS servicios separados en Railway, apuntando al mismo repo.

### Puerto dinámico

Railway inyecta la variable `PORT`. El código la lee:

```python
port = int(os.getenv("PORT", 8000))
uvicorn.run("api:app", host="0.0.0.0", port=port)
```

### Variables de entorno en Railway

Las variables del `.env` local NO están en el repo (está en `.gitignore`). Se configuran manualmente en Railway → servicio → Variables:

```
OPENAI_API_KEY=sk-proj-...
GOOGLE_CREDENTIALS_B64=...    ← credentials.json en base64
GOOGLE_TOKEN_TASKS_B64=...
GOOGLE_TOKEN_CALENDAR_B64=...
GOOGLE_TOKEN_DRIVE_B64=...
```

Las credenciales Google se guardan en base64 porque son archivos JSON con saltos de línea. Al arrancar, `agent_factory.py` las decodifica y escribe a disco.

### Persistencia en Railway

`chroma_db/` y `Knowledge_Base/` son efímeros por defecto — se borran al redesplegar. Para persistencia real: Railway Volumes (Hobby plan). La KB en Markdown sobrevive entre sesiones siempre que no se redespliege; los vectores de ChromaDB se regeneran solos.

## Dos servicios en Railway

```
Proyecto Railway
├── agent_testing  (worker: python telegram_bot.py)  ← bot 24/7
└── agent-api      (web: python api.py)              ← API pública
```

Ambos leen del mismo repo y usan las mismas variables de entorno.

## Documentación de la API

FastAPI genera documentación interactiva automáticamente:
- Swagger UI: `https://tu-dominio.up.railway.app/docs`
- OpenAPI JSON: `https://tu-dominio.up.railway.app/openapi.json`

## Conceptos relacionados

- [[38_message_handler]] — lo que llama la API internamente
- [[09_apis_rest]] — conceptos base de APIs REST
- [[39_telegram_bot]] — el otro canal del sistema
