---
tags: [telegram, bot, polling, webhook, canal]
---

# Bot de Telegram

El bot es uno de los canales del sistema. Permite enviar mensajes de texto y notas de voz desde el teléfono. Toda la lógica de IA está en el MessageHandler — el bot solo maneja la comunicación con Telegram.

## Cómo funciona Telegram Bot API

1. Creas un bot con @BotFather → te da un token
2. Tu servidor llama a la API de Telegram para recibir mensajes (polling) o Telegram llama a tu servidor (webhook)
3. Tu código responde a cada mensaje

## Polling vs Webhook

| | Polling | Webhook |
|--|--|--|
| Quién inicia | Tu servidor pregunta cada N segundos | Telegram envía cuando hay mensaje |
| Requiere URL pública | No | Sí |
| Latencia | ~1-2 segundos | Instantáneo |
| Cuándo usar | Desarrollo local, simplicidad | Producción con servidor web |

**Este proyecto usa polling** — más simple, no requiere configurar URL pública. Railway corre el proceso en background indefinidamente.

## Seguridad — whitelist por user ID

El bot solo responde al propietario. Cualquier otro usuario recibe "No autorizado.":

```python
ALLOWED_USER_ID = int(os.getenv("TELEGRAM_ALLOWED_USER_ID", "0"))

def is_authorized(update: Update) -> bool:
    if ALLOWED_USER_ID == 0:
        return True  # sin restricción si no se configuró
    return update.effective_user.id == ALLOWED_USER_ID
```

Tu ID de Telegram se obtiene escribiéndole a @userinfobot.

## Handlers registrados

```python
app.add_handler(CommandHandler("start",    start_handler))
app.add_handler(CommandHandler("reset",    reset_handler))
app.add_handler(CommandHandler("procesar", procesar_handler))
app.add_handler(MessageHandler(filters.TEXT, text_handler))
app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, voice_handler))
```

| Handler | Qué hace |
|--|--|
| /start | Bienvenida e instrucciones |
| /reset | Limpia historial de conversación |
| /procesar | Dispara el pipeline de MP3 (puede tardar minutos) |
| Texto | handler.process_message(text) |
| Voz/Audio | Descarga archivo → handler.process_voice(path) |

## Flujo de nota de voz

```
Usuario envía nota de voz (.ogg)
        ↓
Bot descarga archivo a temp/tg_{file_id}.ogg
        ↓
handler.process_voice(temp_path)
        ↓
TranscriptionAgent → Whisper-1 → transcript
        ↓
_handle_capture_from_transcript()
        ↓
AnalysisAgent + KnowledgeBaseAgent + re-index
        ↓
"[Guardado] Idea — '...'"
        ↓
Archivo temporal eliminado
```

La voz siempre es CAPTURE — no pasa por classify_intent().

## Variables de entorno necesarias

```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_ALLOWED_USER_ID=1043931661
```

## Conceptos relacionados

- [[38_message_handler]] — el núcleo que llama el bot
- [[12_openai_whisper]] — transcripción de voz
- [[40_fastapi_railway]] — el otro canal del sistema
