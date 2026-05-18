"""
chat.py — Entrypoint CLI del agente conversacional.

Uso:
    python chat.py

Comandos:
    reset   — reinicia el historial de la sesión
    salir   — termina
"""
import os
from dotenv import load_dotenv
from core.agent_factory import build_message_handler


def main() -> None:
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY no configurada en .env")

    handler = build_message_handler(api_key=api_key)

    print("\nListo. Escribe tu pregunta o comparte algo nuevo.")
    print("Comandos: 'reset' = nueva conversacion | 'salir' = terminar\n")
    print("-" * 60)

    while True:
        try:
            user_input = input("Tu: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[chat] Sesion terminada.")
            break

        if not user_input:
            continue

        if user_input.lower() == "salir":
            print("[chat] Hasta luego.")
            break

        if user_input.lower() == "reset":
            handler.reset_conversation()
            print("[chat] Conversacion reiniciada.\n")
            print("-" * 60)
            continue

        response = handler.process_message(user_input)
        print(f"\nAgente: {response}\n")
        print("-" * 60)


if __name__ == "__main__":
    main()
