# Second Brain Agent - Especificacion funcional y tecnica inicial

**Version:** 0.1  
**Fecha:** 2026-05-15  
**Proyecto:** `agent_testing` / futuro `second-brain-agent`  
**Estado:** Borrador para validacion

---

## 1. Resumen ejecutivo

El proyecto **Second Brain Agent** busca construir un asistente personal automatizado capaz de procesar audios, transcripciones y notas de texto para organizar conocimiento, ideas, tareas, reuniones, recordatorios y proyectos.

El sistema nace a partir del uso de BOYA Notra AI como herramienta de captura de voz, pero no debe depender exclusivamente de BOYA. La vision es que cualquier archivo de entrada compatible, como MP3, TXT o MD, pueda ser procesado por un flujo automatico.

La primera version debe validar un flujo funcional minimo: recibir archivos, transcribir audios, interpretar contenido, clasificarlo y generar una base organizada en Markdown, con integracion inicial a Google Tasks y Google Calendar cuando aplique.

---

## 2. Problema a resolver

El usuario captura ideas, pendientes, notas de juntas y reflexiones durante el dia en diferentes momentos: manejando, en el gimnasio, durante llamadas de trabajo o al escuchar podcasts. Actualmente esa informacion queda dispersa en audios, notas sueltas o transcripciones sin estructura.

El problema principal no es solo transcribir audio. El problema real es convertir informacion desordenada en un sistema accionable y consultable.

### Problemas especificos

- Las ideas se pierden o quedan enterradas en audios/transcripts.
- Las tareas derivadas de llamadas o notas no siempre llegan a una lista accionable.
- Las reuniones generan informacion util, pero no necesariamente queda resumida ni organizada.
- Los recordatorios pueden confundirse con tareas o eventos de calendario.
- Los proyectos evolucionan, pero no existe una memoria central que relacione notas, tareas e ideas.
- Crear un archivo por cada idea puede generar caos documental.

---

## 3. Vision del producto

Crear un sistema tipo **segundo cerebro** que funcione como asistente de organizacion personal.

El sistema debe poder recibir contenido no estructurado, interpretarlo, clasificarlo y guardarlo en una estructura organizada que permita:

- Revisar ideas acumuladas.
- Consultar pendientes.
- Obtener resumenes de reuniones.
- Detectar recordatorios.
- Relacionar informacion con proyectos.
- Preparar una futura interfaz conversacional para preguntar sobre lo capturado.

---

## 4. Objetivo de V1

Construir un procesador automatico que tome archivos desde una carpeta de entrada, interprete su contenido y actualice una base de conocimiento en Markdown, Google Tasks y Google Calendar cuando aplique.

### Objetivo minimo de exito

Subir o colocar un archivo MP3, TXT o MD en una carpeta de entrada y obtener automaticamente:

- Transcript si el archivo era audio.
- Clasificacion del contenido.
- Markdown organizado.
- Ideas agregadas al archivo acumulativo de ideas.
- Tareas agregadas a `tasks.md` y Google Tasks.
- Eventos agregados a Google Calendar solo cuando exista fecha y hora clara.
- Reuniones guardadas como archivos individuales.

---

## 5. Alcance de V1

### Incluido

- Procesamiento de archivos MP3.
- Procesamiento de archivos TXT y MD.
- Transcripcion de audio usando OpenAI API en la primera version.
- Analisis de texto usando OpenAI API en la primera version.
- Generacion de Markdown.
- Archivo acumulativo de ideas.
- Archivo acumulativo de tareas.
- Archivo maestro de proyectos.
- Archivo individual por reunion.
- Regla de creacion de Google Tasks.
- Regla de creacion de Google Calendar.
- Identificacion de contenido ambiguo como "requiere revision".
- Arquitectura preparada para cambiar proveedores de transcripcion y analisis.

### Fuera de alcance en V1

- Chat conversacional con el agente.
- WhatsApp, Telegram o Slack.
- App movil propia.
- Dashboard web completo.
- Obsidian plugin.
- LangGraph o sistema multiagente formal en la primera iteracion tecnica.
- Automatizacion cloud completa hasta validar el pipeline.

---

## 6. Entradas soportadas

| Tipo | Descripcion | Accion esperada |
|---|---|---|
| MP3 | Audio de BOYA Notra, llamadas o notas de voz | Transcribir y analizar |
| TXT | Nota de texto simple | Analizar directamente |
| MD | Nota en Markdown | Analizar directamente |

### Carpeta de entrada V1 local

```text
input/
```

### Carpeta de entrada futura en Google Drive

```text
Second_Brain/Inbox/
```

---

## 7. Categorias funcionales

El sistema debe clasificar cada entrada en una categoria principal.

| Categoria | Definicion |
|---|---|
| Idea | Pensamiento, propuesta, inspiracion o concepto nuevo |
| Reunion | Conversacion o junta con puntos, decisiones y acciones |
| Tarea | Accion concreta que debe realizarse |
| Recordatorio | Algo que debe recordarse en una fecha o contexto |
| Proyecto | Iniciativa con continuidad y multiples acciones relacionadas |
| Nota general | Informacion util que no encaja en las categorias anteriores |

Una entrada puede tener una categoria principal y elementos secundarios. Por ejemplo, una reunion puede generar tareas, decisiones, recordatorios e ideas.

---

## 8. Reglas de clasificacion y accion

### 8.1 Ideas

Las ideas no deben generar un archivo separado por cada idea.

Deben agregarse a un archivo acumulativo:

```text
Knowledge_Base/Ideas/ideas.md
```

Formato esperado:

```markdown
## YYYY-MM-DD - Titulo de la idea

**Fuente:** archivo_original.mp3  
**Proyecto relacionado:** Proyecto o No asignado  
**Resumen:** ...  
**Idea:** ...  
**Tags:** #tag1 #tag2
```

---

### 8.2 Tareas

Las tareas deben guardarse en dos lugares:

1. `tasks.md` como historial y contexto.
2. Google Tasks como lista visual accionable.

Archivo acumulativo:

```text
Knowledge_Base/Tasks/tasks.md
```

Regla principal:

- Si se detecta una accion pendiente, se agrega a `tasks.md`.
- Si tiene fecha pero no hora, se crea como Google Task con fecha.
- Si no tiene fecha, se crea como tarea sin fecha o se marca como pendiente sin fecha.
- Si es ambigua, se guarda como "requiere revision".

Ejemplo:

```text
"Mañana revisar lo de SAP"
```

Resultado:

- Entrada en `tasks.md`.
- Google Task con fecha de mañana.

---

### 8.3 Calendario

Google Calendar solo debe usarse cuando exista fecha y hora claras.

Reglas:

| Caso | Accion |
|---|---|
| Fecha pero no hora | Google Tasks |
| Fecha y hora clara | Google Calendar |
| Ambiguo | Markdown como "requiere revision" |

Ejemplos:

```text
"Mañana revisar lo de SAP"
```

Resultado: Google Tasks.

```text
"Mañana a las 4 pm junta con Carlos"
```

Resultado: Google Calendar.

```text
"Luego checar lo de SAP"
```

Resultado: Markdown como requiere revision.

---

### 8.4 Reuniones

Cada reunion debe guardarse como archivo Markdown individual.

Ruta esperada:

```text
Knowledge_Base/Meetings/YYYY-MM-DD_titulo_reunion.md
```

Estructura:

```markdown
# Reunion: Titulo sugerido

## Resumen ejecutivo
## Participantes detectados
## Puntos importantes
## Decisiones
## Acciones para mi
## Acciones para otros
## Riesgos o bloqueos
## Proyectos relacionados
## Transcript completo
```

---

### 8.5 Proyectos

Los proyectos deben gestionarse en un archivo maestro:

```text
Knowledge_Base/Projects/projects.md
```

Reglas:

- Si el usuario menciona explicitamente un proyecto, se debe asociar el contenido a ese proyecto.
- Si no se menciona proyecto, la tarea o idea queda como "No asignado".
- El agente puede sugerir proyectos nuevos, pero no debe crear muchos proyectos basura automaticamente.
- Los proyectos nuevos deben agregarse de forma controlada.

---

### 8.6 Recordatorios

Los recordatorios deben evaluarse segun su nivel de claridad.

- Si el recordatorio tiene fecha y hora clara, crear evento en calendario.
- Si tiene fecha pero no hora, crear tarea en Google Tasks.
- Si es ambiguo, guardarlo como requiere revision.

Archivo de respaldo:

```text
Knowledge_Base/Reminders/reminders.md
```

---

## 9. Estructura esperada de salida

```text
Knowledge_Base/
├── Ideas/
│   └── ideas.md
├── Tasks/
│   └── tasks.md
├── Meetings/
│   └── YYYY-MM-DD_titulo_reunion.md
├── Reminders/
│   └── reminders.md
├── Projects/
│   └── projects.md
├── General_Notes/
│   └── YYYY-MM-DD_titulo_nota.md
├── Transcripts/
│   └── archivo_original_transcript.txt
└── Processed/
    └── archivos_originales_procesados
```

---

## 10. Arquitectura funcional V1

```text
Input folder
    ↓
File Intake
    ↓
Detectar tipo de archivo
    ↓
Si es MP3: transcribir
Si es TXT/MD: leer texto
    ↓
Analizar contenido
    ↓
Clasificar categoria principal
    ↓
Extraer elementos secundarios
    ↓
Actualizar Markdown
    ↓
Crear Google Tasks si aplica
    ↓
Crear Google Calendar event si aplica
    ↓
Mover archivo a procesados
```

---

## 11. Arquitectura tecnica inicial

### 11.1 Servicios intercambiables

El codigo debe estar disenado para no depender permanentemente de OpenAI.

Servicios base:

```text
TranscriptionService
TextAnalysisService
TaskService
CalendarService
FileService
```

Implementaciones iniciales:

```text
OpenAITranscriptionService
OpenAITextAnalysisService
MarkdownFileService
```

Implementaciones futuras:

```text
LocalWhisperTranscriptionService
LocalModelTextAnalysisService
GoogleTasksService
GoogleCalendarService
```

### 11.2 Roadmap tecnico de modelos

| Fase | Transcripcion | Analisis de texto |
|---|---|---|
| V1 inicial | OpenAI API | OpenAI API |
| V1.5 | Whisper local | OpenAI API |
| V2 tecnica | Whisper local | Modelo local via Ollama |

---

## 12. Interaccion con el agente

### V1: agente de fondo

El usuario no conversa con el agente.

El usuario solo coloca archivos en una carpeta de entrada. El sistema procesa y organiza.

```text
Usuario sube archivo
↓
Sistema procesa
↓
Sistema actualiza base de conocimiento
```

### V2: agente consultable

El usuario podra preguntar:

- Que pendientes tengo para manana?
- Que ideas tuve esta semana?
- Que salio de mis reuniones?
- Que dije sobre el proyecto BOYA Agent?
- Que deberia trabajar manana?

### V3: integraciones conversacionales

Opciones futuras:

- Chat web.
- Telegram.
- WhatsApp.
- Slack.
- Interfaz propia.

---

## 13. Requerimientos funcionales V1

| ID | Requerimiento |
|---|---|
| FR-001 | El sistema debe detectar archivos MP3, TXT y MD en una carpeta de entrada. |
| FR-002 | El sistema debe transcribir archivos MP3. |
| FR-003 | El sistema debe leer directamente archivos TXT y MD. |
| FR-004 | El sistema debe clasificar cada entrada en una categoria principal. |
| FR-005 | El sistema debe extraer tareas accionables. |
| FR-006 | El sistema debe extraer ideas y agregarlas a `ideas.md`. |
| FR-007 | El sistema debe crear archivos individuales para reuniones. |
| FR-008 | El sistema debe agregar tareas a `tasks.md`. |
| FR-009 | El sistema debe crear Google Tasks para acciones con fecha o pendientes claros. |
| FR-010 | El sistema debe crear Google Calendar events solo cuando haya fecha y hora claras. |
| FR-011 | El sistema debe marcar contenido ambiguo como "requiere revision". |
| FR-012 | El sistema debe mantener un archivo maestro de proyectos. |
| FR-013 | El sistema debe mover archivos procesados a una carpeta de procesados. |
| FR-014 | El sistema debe evitar procesar dos veces el mismo archivo. |
| FR-015 | El sistema debe guardar transcripts completos. |

---

## 14. Requerimientos no funcionales

| ID | Requerimiento |
|---|---|
| NFR-001 | El sistema debe ser modular y facil de extender. |
| NFR-002 | Las API keys no deben guardarse en el repositorio. |
| NFR-003 | El sistema debe registrar errores sin perder archivos originales. |
| NFR-004 | El sistema debe permitir cambiar proveedor de transcripcion. |
| NFR-005 | El sistema debe permitir cambiar proveedor de analisis de texto. |
| NFR-006 | La salida debe ser legible por humanos. |
| NFR-007 | La estructura de archivos debe ser compatible con Google Drive y Obsidian en el futuro. |

---

## 15. Riesgos y decisiones pendientes

### Riesgos

- Clasificacion incorrecta de tareas o recordatorios.
- Creacion accidental de eventos en calendario.
- Exceso de proyectos sugeridos automaticamente.
- Markdown acumulativo demasiado grande con el tiempo.
- Costos por uso de APIs.
- Privacidad de audios y transcripts.

### Decisiones pendientes

- Definir si Google Tasks se integrara en V1 tecnica o V1.1.
- Definir lista inicial de proyectos activos.
- Definir convencion exacta para nombres de archivos.
- Definir si tareas sin fecha se crean en Google Tasks o solo en Markdown.
- Definir si el usuario quiere una bandeja de revision semanal.

---

## 16. Roadmap propuesto

### Fase 0 - MVP local ya iniciado

- MP3 local en `input/`.
- Transcripcion con OpenAI.
- Analisis con OpenAI.
- Markdown en `output/`.

### Fase 1 - Organizacion Markdown formal

- Crear estructura `Knowledge_Base`.
- Separar ideas, tareas, reuniones, recordatorios y proyectos.
- Actualizar archivos acumulativos.

### Fase 2 - Servicios modulares

- Separar codigo en servicios.
- Preparar interfaces intercambiables.
- Evitar codigo monolitico en `main.py`.

### Fase 3 - Google Tasks y Google Calendar

- Conectar Google Tasks.
- Conectar Google Calendar.
- Aplicar reglas de fecha/hora.

### Fase 4 - Google Drive

- Leer archivos desde Google Drive.
- Escribir Markdown en Google Drive.
- Mover archivos procesados.

### Fase 5 - Cloud Run y Scheduler

- Ejecutar en la nube.
- Programar revisiones periodicas.
- Evitar depender de PC local.

### Fase 6 - Agentes y LangGraph

- Crear Orchestrator.
- Separar agentes por responsabilidad.
- Migrar a LangGraph.

### Fase 7 - Agente consultable

- Indexar Markdown.
- Permitir preguntas sobre ideas, tareas, reuniones y proyectos.

---

## 17. Definicion de exito para V1

La V1 sera exitosa si el usuario puede colocar archivos de audio o texto en una carpeta y obtener, sin organizacion manual:

- Ideas consolidadas.
- Tareas accionables.
- Minutas de reuniones.
- Recordatorios clasificados correctamente.
- Proyectos relacionados.
- Base Markdown organizada y escalable.

El criterio mas importante no es la sofisticacion tecnica, sino que el sistema reduzca la friccion de capturar, organizar y revisar informacion personal.
