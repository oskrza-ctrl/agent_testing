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

**Estado:** Pendiente.

Flujo esperado:

```text
input/audio.mp3
↓
procesar
↓
processed/audio.mp3
```

Reglas:

- Crear carpeta `processed/` si no existe.
- Mover el MP3 solo si el proceso fue exitoso.
- No mover el archivo si ocurre error.
- Evitar sobreescribir archivos con el mismo nombre.

---

## 9. Mejorar CLAUDE.md

**Objetivo:** definir reglas permanentes de trabajo para Claude Code.

**Estado:** Pendiente.

Instrucciones a incluir:

- Mantener el código simple y claro.
- Agregar comentarios breves donde sean útiles.
- No implementar múltiples cambios grandes en una sola iteración.
- Explicar el plan antes de modificar código.
- Resumir cambios después de modificar código.
- No cambiar comportamiento existente sin avisar.
- Sugerir actualización de documentación cuando cambie el alcance.

---

## 10. Agentes con prompts propios

**Objetivo:** convertir los agentes simples en agentes con instrucciones, reglas y criterios propios.

**Estado:** Pendiente.

Estructura esperada:

```text
prompts/
├── orchestrator_agent.md
├── analysis_agent.md
├── task_extraction_agent.md
├── meeting_summary_agent.md
└── markdown_writer_agent.md
```

Ejemplo de comportamiento esperado:

```text
Analysis Agent:
- Clasificar contenido.
- Detectar tareas.
- Detectar recordatorios.
- Detectar proyecto relacionado.
- Marcar información ambigua como “requiere revisión”.
```

---

## 11. Clasificación real por tipo de contenido

**Objetivo:** dejar de generar un Markdown genérico y clasificar cada entrada según su propósito.

**Estado:** Pendiente.

Categorías oficiales:

```text
- Idea
- Reunión
- Tarea
- Recordatorio
- Proyecto
- Nota general
```

Regla importante:

Una entrada puede tener una categoría principal y elementos secundarios.

Ejemplo:

```text
Categoría principal: Reunión

Elementos secundarios:
- Tareas
- Decisiones
- Recordatorios
- Proyectos relacionados
```

---

## 12. Salidas Markdown finales V1

**Objetivo:** escribir la información en una base de conocimiento organizada.

**Estado:** Pendiente.

Estructura esperada:

```text
Knowledge_Base/
├── Ideas/
│   └── ideas.md
├── Tasks/
│   └── tasks.md
├── Meetings/
├── Reminders/
│   └── reminders.md
├── Projects/
│   └── projects.md
└── General_Notes/
```

Reglas:

- Ideas: archivo acumulativo.
- Tareas: archivo acumulativo.
- Reuniones: archivo individual.
- Recordatorios: archivo acumulativo.
- Proyectos: archivo maestro.
- Notas generales: archivo por fecha o categoría.

---

## 13. Integración con Google Tasks

**Objetivo:** crear tareas reales cuando el sistema detecte acciones pendientes.

**Estado:** Pendiente.

Regla funcional:

```text
Si una acción tiene fecha pero no hora → crear Google Task.
```

Ejemplo:

```text
“Mañana revisar lo de SAP”
↓
Google Task con fecha de mañana
```

También debe registrarse en:

```text
Knowledge_Base/Tasks/tasks.md
```

---

## 14. Integración con Google Calendar

**Objetivo:** crear eventos reales cuando el sistema detecte fecha y hora claras.

**Estado:** Pendiente.

Regla funcional:

```text
Si una acción tiene fecha y hora claras → crear evento en Google Calendar.
```

Ejemplo:

```text
“Mañana a las 4 pm junta con Carlos”
↓
Google Calendar event
```

Si la información es ambigua:

```text
Guardar en Markdown como “requiere revisión”.
```

---

## 15. Integración con Google Drive

**Objetivo:** dejar de usar carpetas locales y procesar archivos desde Google Drive.

**Estado:** Pendiente.

Flujo esperado:

```text
Google Drive / Inbox
↓
Procesamiento automático
↓
Knowledge Base en Google Drive
↓
Archivo original movido a Processed
```

Entradas soportadas:

```text
- MP3
- TXT
- MD
```

---

## 16. Migración a LangGraph

**Objetivo:** convertir el flujo de agentes simples en un grafo formal de ejecución.

**Estado:** Pendiente.

Grafo esperado:

```text
intake_node
↓
transcription_node
↓
classification_node
↓
task_node
↓
calendar_node
↓
markdown_node
↓
archive_node
```

Propósito:

- Mejor control del flujo.
- Mejor manejo de estados.
- Mejor capacidad de depuración.
- Preparar el sistema para escenarios más complejos.

---

## 17. Cloud Run + Cloud Scheduler

**Objetivo:** ejecutar el sistema automáticamente sin depender de la PC.

**Estado:** Pendiente.

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

Funcionamiento:

```text
Cada X minutos
↓
Cloud Run despierta
↓
Revisa Drive
↓
Procesa nuevos archivos
↓
Se apaga
```

---

## 18. Agente consultable V2

**Objetivo:** permitir consultas sobre la información organizada.

**Estado:** Futuro.

Ejemplos de preguntas:

```text
¿Qué pendientes tengo para mañana?
¿Qué ideas tuve esta semana?
¿Qué salió de mis reuniones?
¿Qué tengo pendiente del proyecto BOYA?
¿Qué decisiones se tomaron en mis últimas llamadas?
```

Requerimientos probables:

- Indexación de documentos Markdown.
- Búsqueda semántica.
- Memoria consultable.
- Posible base vectorial.

---

## 19. Interfaz conversacional V3

**Objetivo:** interactuar con el sistema de forma natural.

**Estado:** Futuro.

Opciones posibles:

```text
- Chat web
- Telegram
- WhatsApp
- Slack
- App propia
```

Nota:

WhatsApp se considera una integración futura porque puede requerir más configuración y costos adicionales.

---

# Resumen visual

```text
✅ Preparación inicial
✅ Estructura base
✅ API key y configuración
✅ MVP técnico MP3 → transcript → Markdown
✅ Documentación
✅ Servicios
✅ Servicios intercambiables
✅ Primeros agentes simples

➡️ Archive Agent
➡️ CLAUDE.md mejorado
➡️ Prompts propios para agentes
➡️ Clasificación real
➡️ Knowledge Base Markdown
➡️ Google Tasks
➡️ Google Calendar
➡️ Google Drive
➡️ LangGraph
➡️ Cloud Run
➡️ Agente consultable
➡️ Interfaz conversacional
```

---

# Meta actual del proyecto

La meta inmediata es evolucionar el MVP actual hacia una V1 funcional:

```text
Archivos MP3/TXT/MD
↓
Clasificación automática
↓
Organización en Markdown
↓
Google Tasks cuando aplique
↓
Google Calendar cuando aplique
```

La meta futura es construir un sistema consultable tipo segundo cerebro:

```text
Captura
↓
Organización
↓
Memoria
↓
Consulta
↓
Seguimiento
```
