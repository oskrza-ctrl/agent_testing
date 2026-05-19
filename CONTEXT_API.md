# CONTEXT_API.md — Guía técnica para consumir la API del Second Brain Agent

Este archivo es el punto de partida para construir el frontend (Paso 21).
Contiene todo lo necesario para conectarse a la API sin tocar el backend.

---

## Qué es el backend

Sistema personal de conocimiento con IA. El backend:
1. Recibe mensajes de texto y los clasifica (pregunta, captura, acción)
2. Busca en una Knowledge Base con RAG (ChromaDB + embeddings)
3. Captura nueva información y la organiza en categorías
4. Se integra con Google Tasks y Google Calendar

El frontend puede llamar a los endpoints de lectura (`/chat`, `/kb/{category}`) y de escritura (`PATCH /kb/ideas/...`, `PATCH /kb/projects/.../progress`, `POST /kb/projects/.../comments`, `GET /kb/meetings/.../download`).

---

## Base URL

```
https://<tu-dominio>.up.railway.app
```

Reemplaza con la URL del servicio `agent-api` en Railway.
Se obtiene en: Railway → proyecto → servicio `agent-api` → Settings → Networking.

---

## Autenticación

**Por ahora: ninguna.** Cualquier cliente puede llamar a la API.

Cuando se implemente: header `X-API-Key: <clave>` configurada como variable de entorno en Railway.

---

## CORS

Habilitado para todos los orígenes (`*`). El frontend puede llamar desde cualquier dominio sin configuración adicional.

---

## Endpoints

### GET /health

Verifica que el servicio esté vivo.

```
GET /health
```

**Respuesta:**
```json
{"status": "ok"}
```

---

### POST /chat

Envía un mensaje al agente. El backend detecta automáticamente la intención.

```
POST /chat
Content-Type: application/json

{
  "message": "¿qué ideas tengo sobre el proyecto SAT?"
}
```

**Respuesta:**
```json
{
  "response": "Tienes 3 ideas registradas sobre el proyecto SAT: ..."
}
```

**Tipos de mensaje que entiende el agente:**

| Intención | Ejemplos | Qué hace |
|--|--|--|
| QUERY | "¿qué ideas tengo?", "busca notas sobre X" | Busca en la KB con RAG |
| CAPTURE | "idea: usar IA para X", "tarea: llamar a Juan mañana" | Guarda en la KB, crea tarea/evento si aplica |
| ACTION | "marca como completada la tarea X", "archiva los eventos pasados" | Ejecuta acción en Google Tasks/Calendar |
| PIPELINE | "procesa los audios", "revisa el inbox" | Corre el pipeline de MP3 |

El agente siempre responde en español, de forma conversacional.

---

### GET /kb/{category}

Lee el contenido de una categoría de la Knowledge Base.

```
GET /kb/ideas
GET /kb/tasks
GET /kb/reminders
GET /kb/projects
GET /kb/meetings
GET /kb/notes
```

**Categorías acumulativas** (todo en un solo archivo Markdown):
`ideas`, `tasks`, `reminders`, `projects`

Respuesta:
```json
{
  "category": "ideas",
  "content": "# Ideas\n\n## Idea sobre RAG\n**Fecha:** 2026-05-18\n..."
}
```

Si la categoría está vacía:
```json
{
  "category": "ideas",
  "content": ""
}
```

**Categorías individuales** (un archivo por entrada):
`meetings`, `notes`

Respuesta:
```json
{
  "category": "meetings",
  "files": [
    {
      "name": "2026-05-18_reunion_de_equipo.md",
      "content": "# Reunión de equipo\n**Fecha:** 2026-05-18\n..."
    },
    {
      "name": "2026-05-15_revision_proyecto_sat.md",
      "content": "..."
    }
  ]
}
```

Los archivos vienen ordenados del más reciente al más antiguo.

---

### PATCH /kb/ideas/{entry_title}

Edita el campo Resumen de una idea existente, buscándola por su título exacto.
El cambio se persiste en Google Drive automáticamente.

```
PATCH /kb/ideas/Mi%20idea%20sobre%20RAG
Content-Type: application/json

{
  "summary": "nuevo texto del resumen"
}
```

**Respuesta:**
```json
{"ok": true}
```

**Errores:**
- `404` si el archivo de ideas no existe o el título no se encuentra

---

### PATCH /kb/projects/{project_name}/progress

Actualiza o agrega el campo `**Progreso:**` en la entrada del proyecto.
El cambio se persiste en Google Drive automáticamente.

```
PATCH /kb/projects/Proyecto%20SAT/progress
Content-Type: application/json

{
  "progress": 75
}
```

**Respuesta:**
```json
{"ok": true}
```

**Errores:**
- `400` si progress no está entre 0 y 100
- `404` si el proyecto no existe

---

### POST /kb/projects/{project_name}/comments

Agrega un comentario con fecha al final de la entrada del proyecto. Crea la sección `## Comentarios` si no existe.
El cambio se persiste en Google Drive automáticamente.

```
POST /kb/projects/Proyecto%20SAT/comments
Content-Type: application/json

{
  "comment": "Reunión con el cliente aprobada para siguiente semana"
}
```

**Respuesta:**
```json
{"ok": true}
```

Formato del comentario insertado: `- YYYY-MM-DD: texto del comentario`

**Errores:**
- `404` si el proyecto no existe

---

### POST /kb/sync

Fuerza una descarga de la Knowledge Base completa desde Google Drive. Útil para que la API vea capturas nuevas hechas desde Telegram sin necesitar redeploy.

```
POST /kb/sync
```

**Respuesta:**
```json
{"ok": true, "message": "KB sincronizada desde Drive"}
```

Llama este endpoint antes de mostrar cualquier vista de KB si necesitas datos frescos.

---

### GET /kb/meetings/{filename}/download

Descarga el archivo Markdown de una reunión como adjunto.

```
GET /kb/meetings/2026-05-18_reunion_de_equipo.md/download
```

**Respuesta:** archivo `.md` con header:
```
Content-Disposition: attachment; filename="2026-05-18_reunion_de_equipo.md"
Content-Type: text/markdown
```

**Errores:**
- `404` si el archivo no existe

---

## Estructura del Markdown en la KB

### Entradas acumulativas (ideas, tasks, reminders, projects)

Cada entrada está separada por `---` y tiene este formato:

```markdown
## Título de la entrada
**Fecha:** YYYY-MM-DD
**Tags:** tag1 tag2 tag3
**Proyecto:** Nombre del proyecto (o "No asignado")

Resumen del contenido...

### Ideas
- idea 1
- idea 2

### Tareas
- tarea 1
- tarea 2

---

## Siguiente entrada
...
```

### Entradas individuales (meetings, notes)

Archivo completo con nombre `YYYY-MM-DD_titulo.md`:

```markdown
# Título de la reunión/nota
**Fecha:** YYYY-MM-DD
**Categoría:** Reunión
**Tags:** tag1 tag2
**Participantes:** persona1, persona2

## Resumen
...

## Decisiones
- decisión 1

## Acciones
- acción 1 (responsable)

## Próximos pasos
- paso 1
```

---

## Ejemplos de uso — fetch en JavaScript

### Chat básico

```javascript
const res = await fetch('https://tu-api.up.railway.app/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: '¿qué ideas tengo?' })
});
const data = await res.json();
console.log(data.response);
```

### Leer ideas

```javascript
const res = await fetch('https://tu-api.up.railway.app/kb/ideas');
const data = await res.json();
console.log(data.content); // string Markdown
```

### Leer reuniones

```javascript
const res = await fetch('https://tu-api.up.railway.app/kb/meetings');
const data = await res.json();
data.files.forEach(f => {
  console.log(f.name, f.content);
});
```

### Capturar una idea

```javascript
const res = await fetch('https://tu-api.up.railway.app/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ message: 'idea: crear un dashboard de métricas con IA' })
});
const data = await res.json();
// data.response → "[Guardado] Idea — "Dashboard de métricas con IA"\n  Carpeta: Knowledge_Base/Ideas/..."
```

### Editar resumen de una idea

```javascript
await fetch(`https://tu-api.up.railway.app/kb/ideas/${encodeURIComponent(title)}`, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ summary: 'nuevo texto' })
});
```

### Actualizar progreso de un proyecto

```javascript
await fetch(`https://tu-api.up.railway.app/kb/projects/${encodeURIComponent(name)}/progress`, {
  method: 'PATCH',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ progress: 75 })
});
```

### Agregar comentario a un proyecto

```javascript
await fetch(`https://tu-api.up.railway.app/kb/projects/${encodeURIComponent(name)}/comments`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ comment: 'Reunión aprobada para la próxima semana' })
});
```

### Descargar reunión

```javascript
const res = await fetch(`https://tu-api.up.railway.app/kb/meetings/${filename}/download`);
const blob = await res.blob();
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url; a.download = filename; a.click();
```

---

## Errores posibles

| Código | Causa | Solución |
|--|--|--|
| 400 | Mensaje vacío en /chat | Validar que el input no esté vacío antes de enviar |
| 404 | Categoría inválida en /kb | Usar solo: ideas, tasks, meetings, reminders, projects, notes |
| 500 | Error interno (OpenAI, ChromaDB) | Reintentar; si persiste revisar logs en Railway |
| timeout | El agente tarda >30s (pipeline) | Aumentar timeout del fetch; el pipeline puede tardar 1-2 min |

---

## Notas importantes para el frontend

1. **El chat mantiene contexto de conversación** — el QueryAgent recuerda los últimos mensajes de la sesión. Si cierras y reabres la app, el contexto se pierde (el servidor lo mantiene en memoria).

2. **CAPTURE es lento** — guardar una nueva entrada implica llamar a Whisper/GPT + indexar ChromaDB. Espera 3-8 segundos. Muestra un spinner.

3. **PIPELINE es muy lento** — puede tardar 1-2 minutos si hay muchos MP3. No usar en el UI sin feedback claro al usuario.

4. **El contenido de KB es Markdown** — usar una librería como `marked` o `react-markdown` para renderizarlo.

5. **Las categorías de meetings y notes pueden estar vacías** — `files: []` si no hay entradas aún.

6. **Sin estado compartido entre bot y API** — si capturas algo por Telegram, la API lo verá al leer /kb (comparten el mismo filesystem en Railway). Si la API reinicia, ChromaDB se vacía pero la KB en Markdown persiste.

---

## Stack del backend (referencia)

| Componente | Tecnología |
|--|--|
| Framework API | FastAPI |
| Servidor | uvicorn |
| LLM | OpenAI GPT-4o-mini |
| Embeddings | OpenAI text-embedding-3-small |
| Vector store | ChromaDB |
| Transcripción | OpenAI Whisper-1 |
| Despliegue | Railway.app |
| Repo | github.com/oskrza-ctrl/agent_testing |

---

## Sugerencias para el frontend

El frontend ideal tiene estas vistas:

| Vista | Endpoint | Descripción |
|--|--|--|
| Chat | POST /chat | Interfaz conversacional con el agente |
| Ideas | GET /kb/ideas | Lista de ideas parseadas del Markdown |
| Tareas | GET /kb/tasks | Lista de tareas pendientes |
| Reuniones | GET /kb/meetings | Lista de reuniones con buscador |
| Recordatorios | GET /kb/reminders | Recordatorios y deadlines |
| Proyectos | GET /kb/projects | Estado de proyectos activos |

**Stack recomendado para el frontend:**
- React + Vite (rápido de levantar)
- TailwindCSS (estilo sin fricción)
- `react-markdown` para renderizar el contenido de la KB
- Desplegado en Vercel o Railway (tercer servicio)
