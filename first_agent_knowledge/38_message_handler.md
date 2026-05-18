---
tags: [message-handler, canal-agnostico, factory, arquitectura]
---

# MessageHandler — núcleo canal-agnóstico

## El problema que resuelve

Sin MessageHandler, cada canal (terminal, Telegram, API) tendría que reimplementar la misma lógica: clasificar intención, llamar agentes, manejar errores. Cualquier cambio habría que hacerlo en 3 lugares.

Con MessageHandler, la lógica vive en un solo lugar y cada canal solo llama `process_message()`.

## Qué es canal-agnóstico

El MessageHandler no sabe ni le importa desde dónde viene el mensaje:

```python
# Desde terminal (chat.py)
response = handler.process_message("¿qué ideas tengo?")

# Desde Telegram (telegram_bot.py)
response = handler.process_message(update.message.text)

# Desde API HTTP (api.py)
response = handler.process_message(req.message)
```

Todos reciben el mismo resultado. El canal solo se encarga de mostrar la respuesta.

## Métodos públicos

```python
handler.process_message(text)     # texto → clasifica → responde
handler.process_voice(file_path)  # audio → transcribe → CAPTURE
handler.run_pipeline()            # dispara main.py → resumen con GPT
handler.reset_conversation()      # limpia historial de conversación
```

## Dependencias inyectadas

El MessageHandler no crea sus dependencias — las recibe:

```python
MessageHandler(
    openai_client,
    rag_service,
    query_agent,
    analysis_agent,
    markdown_agent,
    kb_agent,
    kb_dir,
    output_dir,
    transcription_agent,  # opcional
    tasks_agent,          # opcional
    calendar_agent,       # opcional
)
```

Esto permite testear, cambiar proveedores o deshabilitar integraciones sin tocar el núcleo.

## agent_factory.py — el inicializador

Construir el MessageHandler a mano sería repetitivo en cada entrypoint. La factory lo hace una vez:

```python
# En cualquier entrypoint
handler = build_message_handler(api_key=os.getenv("OPENAI_API_KEY"))
```

`build_message_handler()` en `core/agent_factory.py`:
1. Crea el cliente OpenAI
2. Inicializa ChromaDB e indexa la KB
3. Crea todos los agentes
4. Intenta crear agentes Google (silencioso si no hay credenciales)
5. Retorna el MessageHandler listo

## Flujo interno de process_message()

```
texto
  ↓
classify_intent()  → QUERY / CAPTURE / PIPELINE / ACTION
  ↓
QUERY    → query_agent.chat(text)           → respuesta RAG
CAPTURE  → analysis_agent + kb_agent + ...  → "[Guardado] ..."
PIPELINE → subprocess main.py + GPT summary → resumen conversacional
ACTION   → classify_action() → tasks/calendar agent
```

## Conceptos relacionados

- [[37_intent_classifier]] — el clasificador que usa internamente
- [[20_arquitectura_servicios]] — los servicios que inyecta
- [[21_arquitectura_agentes]] — los agentes que orquesta
- [[39_telegram_bot]] — uno de los canales que lo consume
- [[40_fastapi_railway]] — otro canal que lo consume
