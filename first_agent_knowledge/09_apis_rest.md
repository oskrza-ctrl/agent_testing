---
tags: [api, rest, http, json, fundamentos]
---

# Qué es una API REST

Una API (Application Programming Interface) es un contrato que permite que dos programas se comuniquen. REST es el estilo arquitectónico más común para APIs web.

## La analogía del restaurante

- Tú eres el cliente (tu código Python)
- El mesero es la API (OpenAI API, Google Tasks API)
- La cocina es el servidor remoto (los servidores de OpenAI / Google)
- El menú es la documentación de la API

Haces un pedido (request) → el mesero lo lleva a cocina → te trae el resultado (response).

## HTTP: el protocolo de comunicación

Una petición HTTP tiene:

```
Método: POST
URL: https://api.openai.com/v1/audio/transcriptions
Headers:
  Authorization: Bearer sk-proj-...
  Content-Type: multipart/form-data
Body:
  file: [archivo mp3]
  model: whisper-1
```

Los métodos más comunes:
- `GET` — obtener datos (sin modificar nada)
- `POST` — enviar datos / crear algo
- `PATCH` / `PUT` — actualizar algo
- `DELETE` — eliminar algo

## Status codes

```
200 OK         — todo bien
201 Created    — recurso creado exitosamente
400 Bad Request — el cliente envió algo mal
401 Unauthorized — falta autenticación
403 Forbidden  — autenticado pero sin permisos
404 Not Found  — el recurso no existe
429 Too Many Requests — superaste el rate limit
500 Internal Server Error — el servidor falló
```

## JSON — el formato de datos

Las APIs modernas intercambian datos en JSON (JavaScript Object Notation):

```json
{
  "category": "Reunión",
  "title": "Revisión del proyecto BOYA",
  "tasks": ["Enviar resumen a equipo", "Agendar siguiente reunión"],
  "tags": ["#boya", "#reunion"]
}
```

En Python, JSON se convierte a dict con `json.loads()` y de dict a JSON con `json.dumps()`.

## Cómo el proyecto usa APIs REST

```
Audio MP3
  |
  v (POST a OpenAI Whisper)
Texto transcript
  |
  v (POST a OpenAI GPT-4o-mini)
JSON con AnalysisResult
  |
  v (POST a Google Tasks API)
Tarea creada en Google Tasks
```

## Conceptos relacionados

- [[10_autenticacion_apis]] — cómo autenticarse en una API
- [[11_openai_overview]] — la API de OpenAI en detalle
- [[15_google_apis_overview]] — las APIs de Google usadas en el proyecto
