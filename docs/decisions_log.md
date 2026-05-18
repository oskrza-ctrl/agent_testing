# Decisions Log

Registro cronológico de decisiones importantes tomadas en el proyecto.

---

## 2026-05-12

### DEC-001 — Stack inicial del proyecto

**Decisión:** Usar Python como lenguaje principal del proyecto.  
**Razón:** Ecosistema maduro para IA, compatibilidad con OpenAI SDK, rapidez para prototipar.

---

### DEC-002 — Proveedor de transcripción inicial

**Decisión:** Usar OpenAI Whisper API (`whisper-1`) para transcripción de audio.  
**Razón:** Es el modelo más económico disponible (~$0.006/min), confiable y fácil de integrar. Se evaluarán alternativas (Deepgram, AssemblyAI) si el costo escala.  
**Revisión futura:** Migrar a Whisper local en Fase 1.5 para eliminar costo por token.

---

### DEC-003 — Modelo de análisis de texto

**Decisión:** Usar `gpt-4o-mini` para análisis del transcript y generación de Markdown.  
**Razón:** Relación costo/calidad superior a `gpt-4o` para tareas de clasificación y resumen de texto. Mucho más económico (~$0.15 vs $2.50 por millón de tokens de entrada).

---

### DEC-004 — Sin cloud ni LangGraph en V1

**Decisión:** Validar el pipeline completamente local antes de agregar complejidad.  
**Razón:** Reducir variables de fallo, iterar rápido y entender el flujo antes de distribuirlo.  
**Alcance:** Sin Google Drive, sin Cloud Run, sin LangGraph hasta que el flujo local sea estable.

---

### DEC-005 — Salida en Markdown plano

**Decisión:** Usar archivos Markdown como formato de salida principal, sin base de datos.  
**Razón:** Legible por humanos, compatible con Obsidian, compatible con Google Drive y fácil de versionar con git.

---

## 2026-05-14

### DEC-006 — Arquitectura de servicios modulares

**Decisión:** Diseñar el código con interfaces de servicio intercambiables desde el inicio.  
**Razón:** Evitar dependencia permanente de OpenAI. El sistema debe poder cambiar de proveedor de transcripción o análisis sin reescribir el pipeline.  
**Servicios definidos:** `TranscriptionService`, `TextAnalysisService`, `FileService`, `TaskService`, `CalendarService`.

---

### DEC-007 — Regla de calendario vs. tareas

**Decisión:** Crear eventos en Google Calendar solo cuando exista fecha **y** hora explícitas. Con fecha pero sin hora → Google Tasks. Ambiguo → Markdown como "requiere revisión".  
**Razón:** Evitar creación accidental de eventos en calendario que contaminen la agenda.

---

### DEC-008 — Ideas en archivo acumulativo, no archivos separados

**Decisión:** Las ideas se agregan a `ideas.md` en lugar de crear un archivo por cada idea.  
**Razón:** Evitar caos documental. Un archivo acumulativo es más fácil de revisar y mantener.

---

### DEC-009 — Documentación viva en el repositorio

**Decisión:** Mantener `docs/` como fuente de verdad del proyecto dentro del repo.  
**Razón:** La documentación debe evolucionar junto con el código y ser revisable antes de implementar cambios de alcance.  
**Archivos base:**
- `second_brain_agent_functional_spec.md` — alcance funcional
- `technical_spec.md` — arquitectura técnica
- `roadmap.md` — fases de desarrollo
- `decisions_log.md` — este archivo

---

## 2026-05-15

### DEC-010 — Análisis con respuesta JSON estructurada

**Decisión:** Usar `response_format={"type": "json_object"}` en la llamada a OpenAI para que el modelo devuelva siempre un JSON válido con campos definidos, en lugar de texto libre o Markdown.  
**Razón:** El Markdown libre era difícil de parsear de forma confiable. Un JSON con campos explícitos (`category`, `tasks`, `reminders`, etc.) permite que el código procese la respuesta de forma robusta sin regex ni heurísticas frágiles.

---

### DEC-011 — No inventar fechas absolutas a partir de referencias relativas

**Decisión:** El `analysis_agent.md` prohíbe explícitamente convertir referencias relativas ("mañana", "el viernes", "la próxima semana") en fechas absolutas inventadas.  
**Razón:** En pruebas reales, GPT generaba fechas del pasado (ej: 2023-10-12) para referencias como "mañana". Esto contaminaría Google Calendar con eventos en fechas incorrectas. La referencia original del usuario se preserva y se marca como candidato (`[candidato: Google Calendar]` o `[candidato: Google Tasks]`).

---

### DEC-012 — Enrutado de elementos secundarios desde Reuniones y Notas generales

**Decisión:** Cuando la categoría principal es Reunión o Nota general, las tareas, recordatorios e ideas detectadas como elementos secundarios se escriben también en sus archivos acumulativos (`tasks.md`, `reminders.md`, `ideas.md`).  
**Razón:** Sin este enrutado, una tarea capturada dentro de una reunión solo existía en el archivo de la reunión y nunca llegaba a la lista de tareas accionable. El enrutado secundario garantiza que ningún elemento accionable se pierda independientemente de la categoría principal.

---

### DEC-013 — Formato enriquecido para archivos de Reunión

**Decisión:** Los archivos individuales de Reunión incluyen secciones explícitas: Participantes, Decisiones, Acciones para mí, Acciones para otros, Riesgos y bloqueos, Próximos pasos.  
**Razón:** El formato genérico anterior no capturaba la riqueza de información de una reunión. Las secciones específicas permiten recuperar información accionable directamente sin releer el transcript completo. Si un campo no se detecta, se escribe "No detectado".

---

### DEC-014 — Tags obligatorios en toda salida

**Decisión:** El prompt del agente exige siempre entre 2 y 5 tags. Si el contenido es muy genérico y no hay tags específicos, se usan tags de fallback: `#nota-general`, `#sin-proyecto`, `#requiere-revision`.  
**Razón:** En pruebas iniciales algunos archivos se generaban sin tags. Los tags son esenciales para la búsqueda futura en la Knowledge Base (Fase 18 — Agente consultable). Establecer la regla desde ahora evita tener que re-procesar entradas en el futuro.

---

### DEC-015 — Google Tasks con prefijo de proyecto y due date de 7 días por default

**Decisión:** Las tareas creadas en Google Tasks incluyen el nombre del proyecto como prefijo `[Proyecto]` en el título. Las tareas sin fecha explícita reciben un due date de 7 días desde el día de procesamiento.  
**Razón:** Sin prefijo, una lista con muchas tareas pierde contexto. Con `[SAT] Revisar pendientes` el origen es inmediatamente visible. El due date de 7 días evita que las tareas sin fecha queden flotando indefinidamente sin una fecha de revisión.

---

### DEC-016 — Google Calendar usa result.title como título del evento

**Decisión:** El título del evento en Google Calendar se toma de `result.title` (generado por el agente de análisis), no del texto crudo del recordatorio.  
**Razón:** El texto crudo del recordatorio suele incluir marcadores como `[candidato: Google Calendar]` y referencias de tiempo que quedan mal como título de evento. `result.title` es siempre limpio, descriptivo y generado específicamente para ser un título.

---

### DEC-017 — Credenciales Google opcionales, sistema degradado graciosamente

**Decisión:** Google Tasks y Google Calendar son integraciones opcionales. Si `credentials/credentials.json` no existe, el sistema procesa normalmente y solo omite la creación de tareas y eventos.  
**Razón:** Permite que el sistema funcione en cualquier entorno (PC sin credenciales, CI, pruebas) sin errores ni configuración obligatoria. La Knowledge Base local siempre funciona.

---

### DEC-018 — Drive como capa de I/O opcional sin modificar el pipeline

**Decisión:** Google Drive se integra como una capa de entrada/salida opcional que rodea el pipeline, sin modificar ningún agente existente. Si los folder IDs no están configurados en `.env`, el sistema usa carpetas locales normalmente.  
**Razón:** Mantener el pipeline desacoplado del proveedor de almacenamiento. El mismo código funciona en modo local (desarrollo) y en modo Drive (producción) sin cambiar lógica de negocio.

---

### DEC-019 — KB se sincroniza a Drive archivo por archivo tras cada procesamiento

**Decisión:** En lugar de sincronizar toda la Knowledge Base al final, cada archivo KB modificado se sube a Drive inmediatamente después de procesarse el audio correspondiente.  
**Razón:** Si el proceso falla a mitad de un lote, los archivos ya procesados están seguros en Drive. Una sincronización al final del lote perdería todos los resultados si el sistema falla en el último audio.

---

### DEC-020 — Upload actualiza el archivo existente en Drive, no duplica

**Decisión:** Antes de subir un archivo KB a Drive, se verifica si ya existe con el mismo nombre en la carpeta. Si existe, se actualiza; si no, se crea.  
**Razón:** Los archivos acumulativos (`ideas.md`, `tasks.md`) se actualizan con cada procesamiento. Sin esta verificación, cada ejecución crearía una copia nueva en Drive generando duplicados.

---

### DEC-021 — LangGraph como orquestador, agentes sin cambios

**Decisión:** LangGraph reemplaza la orquestación imperativa en `_process_one()` sin modificar ningún agente existente. Los agentes se convierten en nodos mediante funciones factory que los envuelven.  
**Razón:** Separar la lógica de negocio (agentes) del flujo de ejecución (grafo). Si en el futuro se agregan ramas condicionales, paralelización o checkpointing, solo cambia el grafo, no los agentes.

---

### DEC-022 — Error en cualquier nodo detiene el pipeline sin mover el MP3

**Decisión:** Si un nodo setea `state["error"]`, todos los nodos siguientes hacen early return `{}`. El nodo `archive_node` también hace early return, por lo que el MP3 queda en `input/` para revisión manual.  
**Razón:** Comportamiento idéntico al pipeline anterior: un error en transcripción o análisis nunca debe mover el archivo original, garantizando que se pueda reintentar.

---

### DEC-023 — Nodos opcionales verifican existencia del agente en tiempo de ejecución

**Decisión:** Los nodos de Drive, Tasks y Calendar verifican `if not agent: return {}` al inicio. No usan edges condicionales de LangGraph para simplificar el grafo.  
**Razón:** Un grafo lineal es más fácil de mantener y depurar que uno con múltiples ramas condicionales. La condicionalidad está en el nodo, no en el grafo.

---

## 2026-05-15 (continuación)

### DEC-024 — RAG con ChromaDB para agente consultable

**Decisión:** Usar ChromaDB como vector store local y `text-embedding-3-small` de OpenAI para indexar la Knowledge Base y permitir búsqueda semántica.  
**Razón:** ChromaDB es gratuito, local, persistente y fácil de integrar. `text-embedding-3-small` cuesta ~$0.02/M tokens — prácticamente cero para uso personal. No se requiere infraestructura externa.  
**Diseño:** La colección se recrea completa al arrancar `chat.py` para garantizar que siempre refleje el estado actual de la KB.

---

### DEC-025 — Modo dual QUERY/CAPTURE con clasificador GPT

**Decisión:** El `chat.py` detecta automáticamente si el usuario está haciendo una pregunta (QUERY) o compartiendo contenido nuevo (CAPTURE) usando GPT-4o-mini como clasificador de intención.  
**Razón:** Evita que el usuario tenga que usar comandos explícitos o dos entrypoints distintos. Una sola conversación libre maneja ambos modos. GPT clasifica mejor que reglas de texto porque entiende el contexto semántico ("tuve una reunión hoy" → CAPTURE, aunque no empiece con "idea:").

---

### DEC-026 — Re-indexado inmediato tras captura de texto

**Decisión:** Después de cada captura de texto, `chat.py` re-indexa la Knowledge Base completa en ChromaDB.  
**Razón:** Sin re-indexado, el contenido recién capturado no aparece en las consultas de la misma sesión. El re-indexado completo tarda < 2 segundos con el volumen actual, por lo que no justifica una solución incremental más compleja.

---

## 2026-05-18

### DEC-027 — process_message() como función central canal-agnóstica

**Decisión:** Extraer toda la lógica de decisión (QUERY vs CAPTURE) al `MessageHandler` en `core/message_handler.py`. Cada canal (CLI, Telegram, futura app) solo llama `handler.process_message(text)` y recibe una respuesta en texto.  
**Razón:** Evita duplicar lógica entre entrypoints. Cuando se agrega un nuevo canal solo se escribe el adaptador de entrada/salida, no la lógica de negocio.

---

### DEC-028 — Telegram en modo polling para desarrollo

**Decisión:** `telegram_bot.py` usa polling (`app.run_polling()`) en lugar de webhook.  
**Razón:** Polling no requiere URL pública ni infraestructura desplegada. Funciona localmente desde cualquier PC. El webhook se activará cuando se implemente Cloud Run (paso 17).

---

### DEC-029 — Audios de Telegram siempre son CAPTURE

**Decisión:** Los mensajes de voz de Telegram siempre se procesan como captura (transcripción → análisis → KB). No pasan por el clasificador de intención.  
**Razón:** Un audio de voz es siempre contenido nuevo — no tiene sentido que alguien mande una nota de voz para "hacer una pregunta" cuando puede escribirla. Esto simplifica el flujo y evita clasificaciones erróneas.

---

### DEC-030 — Whitelist de usuario en Telegram via TELEGRAM_ALLOWED_USER_ID

**Decisión:** El bot verifica que el `user.id` del remitente coincida con `TELEGRAM_ALLOWED_USER_ID` antes de procesar cualquier mensaje. Si no coincide, responde "No autorizado."  
**Razón:** Sin esta restricción el bot es completamente público — cualquiera que conozca el username puede consultar o modificar la Knowledge Base del usuario.

---

## Plantilla para nuevas decisiones

```markdown
### DEC-XXX — Título de la decisión

**Decisión:** Qué se decidió hacer o no hacer.  
**Razón:** Por qué se tomó esta decisión.  
**Revisión futura:** Cuándo o bajo qué condición se debería reconsiderar (opcional).
```
