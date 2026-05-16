---
tags: [decisiones, arquitectura, historia, contexto, adr]
---

# Las decisiones técnicas del proyecto

Este documento resume las 23 decisiones más importantes tomadas durante el desarrollo. Cada una tiene contexto: qué se decidió, por qué, y qué alternativas se descartaron.

## DEC-001 — Python como lenguaje principal
Python tiene el ecosistema de IA más maduro. Compatibilidad nativa con OpenAI SDK, prototyping rápido. JavaScript fue descartado por ecosistema de IA menos maduro.

## DEC-002 — Whisper-1 para transcripción
`whisper-1` a $0.006/min es el modelo más económico disponible. Se evaluaron Deepgram y AssemblyAI pero son más caros para el volumen esperado. La decisión incluye un plan de migración a Whisper local para eliminar el costo.

## DEC-003 — GPT-4o-mini para análisis
`gpt-4o-mini` es ~16x más barato que `gpt-4o` ($0.15 vs $2.50 por millón de tokens de entrada) para tareas de clasificación y resumen. La calidad es suficiente para notas personales.

## DEC-004 — Sin cloud ni LangGraph en V1
El principio de "validar local antes de agregar complejidad". Se usó código Python simple hasta que el flujo estuvo estable.

## DEC-005 — Salida en Markdown plano
Markdown es legible sin herramientas, compatible con Obsidian, versionable con git. Se descartaron bases de datos (Notion, SQLite) para la primera versión.

## DEC-006 — Arquitectura de servicios intercambiables
Las interfaces abstractas (`TranscriptionService`, `AnalysisService`) permiten cambiar proveedor sin modificar el pipeline. Ver [[20_arquitectura_servicios]].

## DEC-007 — Regla de calendario vs tareas
Solo se crean eventos en Calendar cuando hay fecha Y hora explícitas. Fecha sin hora → Google Tasks. Ambiguo → solo Markdown. Evita contaminar el calendario con eventos en fechas incorrectas.

## DEC-008 — Ideas en archivo acumulativo
Un solo `ideas.md` en lugar de un archivo por idea. Evita el caos documental. Es más fácil revisar un archivo que buscar entre decenas.

## DEC-009 — Documentación viva en el repositorio
`docs/` como fuente de verdad. La documentación evoluciona con el código, no en Notion o una wiki externa.

## DEC-010 — Respuesta JSON estructurada
`response_format={"type": "json_object"}` fuerza a GPT a devolver JSON parseable. Elimina el parsing frágil de texto libre con regex. Ver [[14_openai_json_mode]].

## DEC-011 — No inventar fechas absolutas
GPT tenía el bug de convertir "mañana" en "2023-10-12" (fechas del pasado). La regla explícita en el prompt lo corrige: se preserva el texto original y se marca con `[candidato: ...]`. Ver [[27_reglas_calendario_tareas]].

## DEC-012 — Enrutado secundario desde Reuniones
Las tareas e ideas encontradas dentro de una reunión también van a sus archivos acumulativos. Sin esto, una tarea capturada en una reunión nunca llegaría a la lista de tareas accionable. Ver [[25_knowledge_base]].

## DEC-013 — Formato enriquecido para Reuniones
Los archivos de Reunión tienen secciones explícitas: Participantes, Decisiones, Acciones para mí, Acciones para otros, Riesgos, Próximos pasos. El formato genérico no capturaba la riqueza de una reunión.

## DEC-014 — Tags obligatorios en toda salida
Mínimo 2 tags por entrada. Tags de fallback: `#nota-general`, `#sin-proyecto`, `#requiere-revision`. Sin esto algunos archivos se generaban sin tags, dificultando la búsqueda futura en Obsidian.

## DEC-015 — Google Tasks con prefijo de proyecto y due date de 7 días
`[BOYA] Revisar el contrato` — el proyecto es visible de inmediato. Due date de 7 días evita tareas flotando indefinidamente.

## DEC-016 — result.title como título del evento de Calendar
El texto crudo del recordatorio incluye marcadores y referencias de tiempo que quedan mal como título de evento. `result.title` es siempre limpio.

## DEC-017 — Credenciales Google opcionales
Si `credentials.json` no existe, el sistema funciona con solo OpenAI y KB local. Permite operar en cualquier entorno sin configuración obligatoria.

## DEC-018 — Drive como capa de I/O opcional
Drive rodea el pipeline sin modificar ningún agente. El mismo código funciona en modo local y modo Drive. Ver [[19_google_drive_api]].

## DEC-019 — Sincronización a Drive archivo por archivo
Se sube cada archivo KB después de procesar cada MP3, no al final del batch. Si el proceso falla a mitad, los archivos ya procesados están seguros en Drive.

## DEC-020 — Upload actualiza el archivo existente en Drive
Antes de subir, verificar si ya existe el archivo. Si sí, actualizar; si no, crear. Evita duplicar archivos acumulativos (`ideas.md`, `tasks.md`) con cada ejecución.

## DEC-021 — LangGraph como orquestador, agentes sin cambios
LangGraph reemplaza el código imperativo en `_process_one()` sin modificar ningún agente. Los agentes se convierten en nodos mediante factory functions. Ver [[31_langgraph_pipeline]].

## DEC-022 — Error en cualquier nodo detiene el pipeline sin mover el MP3
Si un nodo setea `state["error"]`, los nodos siguientes hacen early return. El MP3 queda en `input/` para reintento manual. Ver [[28_manejo_errores_pipeline]].

## DEC-023 — Nodos opcionales verifican existencia del agente en tiempo de ejecución
Los nodos opcionales (Drive, Tasks, Calendar) verifican `if not agent: return {}` en lugar de usar edges condicionales de LangGraph. Un grafo lineal es más fácil de mantener que uno con múltiples ramas.

---

## Conceptos relacionados

- [[33_vision_second_brain]] — la visión que guió estas decisiones
- [[20_arquitectura_servicios]] — DEC-006, DEC-017
- [[29_langgraph_intro]] — DEC-021
- [[27_reglas_calendario_tareas]] — DEC-007, DEC-011, DEC-015, DEC-016
