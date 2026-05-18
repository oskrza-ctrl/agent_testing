"""
telegram_bot.py — Entrypoint del bot de Telegram (modo polling).

Uso:
    python telegram_bot.py

Requiere en .env:
    TELEGRAM_BOT_TOKEN=tu_token_de_botfather
    TELEGRAM_ALLOWED_USER_ID=tu_id_de_telegram

Comandos disponibles en Telegram:
    /start  — bienvenida e instrucciones
    /reset  — reinicia el historial de conversación

Mensajes soportados:
    Texto   — pregunta o captura (el agente detecta la intención)
    Voz     — siempre se transcribe y guarda en la Knowledge Base
"""
import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from core.agent_factory import build_message_handler

load_dotenv()

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

ALLOWED_USER_ID = int(os.getenv("TELEGRAM_ALLOWED_USER_ID", "0"))

# Handler compartido — se inicializa una vez al arrancar el bot
_handler = None


def get_handler():
    global _handler
    if _handler is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY no configurada en .env")
        logger.info("Inicializando agentes...")
        _handler = build_message_handler(api_key=api_key)
        logger.info("Agentes listos.")
    return _handler


def is_authorized(update: Update) -> bool:
    if ALLOWED_USER_ID == 0:
        return True  # sin restricción si no se configuró el ID
    return update.effective_user.id == ALLOWED_USER_ID


# ── Handlers de Telegram ──────────────────────────────────────────

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        await update.message.reply_text("No autorizado.")
        return

    await update.message.reply_text(
        "Hola! Soy tu Second Brain.\n\n"
        "Puedes:\n"
        "- Escribirme una idea, tarea, recordatorio o nota para guardarla\n"
        "- Hacerme una pregunta sobre lo que tienes guardado\n"
        "- Enviarme una nota de voz para transcribirla y guardarla\n"
        "- Pedirme que procese los audios del inbox\n\n"
        "/procesar — procesa los MP3s del Drive Inbox\n"
        "/reset — reinicia la conversacion\n"
    )


async def reset_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        await update.message.reply_text("No autorizado.")
        return
    get_handler().reset_conversation()
    await update.message.reply_text("Conversacion reiniciada.")


async def procesar_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        await update.message.reply_text("No autorizado.")
        return
    await update.message.reply_text("Procesando audios del Inbox... esto puede tomar unos minutos.")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    try:
        response = get_handler().run_pipeline()
    except Exception as e:
        response = f"Error al procesar: {e}"
    await update.message.reply_text(response)


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        await update.message.reply_text("No autorizado.")
        return

    text = update.message.text.strip()
    if not text:
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    try:
        response = get_handler().process_message(text)
    except Exception as e:
        logger.exception("Error procesando mensaje de texto")
        response = f"Ocurrio un error: {e}"

    await update.message.reply_text(response)


async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_authorized(update):
        await update.message.reply_text("No autorizado.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    file_obj  = update.message.voice or update.message.audio
    file_id   = file_obj.file_id
    extension = ".ogg" if update.message.voice else ".mp3"
    temp_path = TEMP_DIR / f"tg_{file_id}{extension}"

    try:
        tg_file = await context.bot.get_file(file_id)
        await tg_file.download_to_drive(temp_path)
        response = get_handler().process_voice(temp_path)
    except Exception as e:
        logger.exception("Error procesando audio")
        response = f"Ocurrio un error procesando el audio: {e}"
    finally:
        if temp_path.exists():
            temp_path.unlink()

    await update.message.reply_text(response)


# ── Main ──────────────────────────────────────────────────────────

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN no configurado en .env\n"
            "Crea un bot con @BotFather en Telegram y agrega el token."
        )

    get_handler()

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start",    start_handler))
    app.add_handler(CommandHandler("reset",    reset_handler))
    app.add_handler(CommandHandler("procesar", procesar_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, voice_handler))

    logger.info("Bot iniciado — solo usuario %d autorizado.", ALLOWED_USER_ID)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
