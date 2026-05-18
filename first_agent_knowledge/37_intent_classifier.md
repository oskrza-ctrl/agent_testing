---
tags: [intent, clasificador, routing, dos-niveles, gpt]
---

# Clasificador de intención — dos niveles

El clasificador determina qué quiere hacer el usuario con cada mensaje y lo enruta al agente correcto. Es el primer paso de `process_message()`.

## Por qué un clasificador

El agente no sabe si "¿qué ideas tengo?" es una pregunta o si "tengo una idea sobre X" es una captura. GPT-4o-mini lo determina en una sola llamada con temperatura=0.

## Nivel 1 — classify_intent()

Archivo: `services/rag/intent_classifier.py`

```
mensaje del usuario
        ↓
GPT-4o-mini (temperature=0)
        ↓
QUERY | CAPTURE | PIPELINE | ACTION
```

| Intent | Cuándo | Ejemplo |
|--|--|--|
| QUERY | Pregunta sobre la KB | "¿qué ideas tengo?", "busca notas sobre X" |
| CAPTURE | Información nueva para guardar | "idea: usar IA para...", "tarea: llamar a Juan" |
| PIPELINE | Quiere procesar audios del inbox | "procesa los audios", "revisa el inbox" |
| ACTION | Quiere ejecutar una acción sobre datos existentes | "marca como completada la tarea X", "archiva eventos pasados" |

## Nivel 2 — classify_action()

Solo se ejecuta si el Nivel 1 devuelve ACTION.

Archivo: `services/rag/action_classifier.py`

```
mensaje de acción
        ↓
GPT-4o-mini (temperature=0)
        ↓
COMPLETE_TASK | ARCHIVE_EVENTS
```

| Action | Qué hace |
|--|--|
| COMPLETE_TASK | Lista tareas pendientes → GPT elige cuál coincide → marca como completada |
| ARCHIVE_EVENTS | Lista eventos pasados del calendario → los borra todos |

## Flujo completo en MessageHandler

```python
def process_message(self, text):
    intent = classify_intent(self.client, text)    # Nivel 1

    if intent == "PIPELINE":  return self.run_pipeline()
    if intent == "CAPTURE":   return self._handle_capture(text)
    if intent == "ACTION":    return self._handle_action(text)
    return self.query_agent.chat(text)  # QUERY por defecto

def _handle_action(self, text):
    action = classify_action(self.client, text)    # Nivel 2

    if action == "COMPLETE_TASK":   return self.tasks_agent.find_and_complete(text, self.client)
    if action == "ARCHIVE_EVENTS":  return self.calendar_agent.archive_past_events()
```

## Por qué dos niveles

Un solo clasificador con muchas categorías se vuelve inestable — GPT puede confundirse entre opciones similares. Separar en dos niveles especializados es más robusto:

- Nivel 1: distingue el tipo de operación (lectura, escritura, acción, pipeline)
- Nivel 2: dentro de "acción", determina cuál específicamente

Escala limpiamente: si mañana agregas "borrar tarea", solo tocas el Nivel 2.

## Conceptos relacionados

- [[38_message_handler]] — dónde vive el routing completo
- [[36_chromadb_rag]] — a dónde van los mensajes QUERY
- [[21_arquitectura_agentes]] — los agentes que reciben cada intent
