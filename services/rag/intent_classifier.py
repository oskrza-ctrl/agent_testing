from openai import OpenAI

_SYSTEM = """Clasifica el mensaje del usuario como:

- CAPTURE: el usuario está compartiendo información nueva — una idea, tarea, recordatorio,
  nota de reunión, proyecto o cualquier contenido que debe guardarse en su base de conocimiento.

- QUERY: el usuario está haciendo una pregunta, buscando información o pidiendo un resumen
  de algo que ya está en su base de conocimiento.

Responde ÚNICAMENTE con la palabra CAPTURE o QUERY, sin explicación."""


def classify_intent(client: OpenAI, message: str) -> str:
    """Returns 'CAPTURE' or 'QUERY'."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user",   "content": message},
        ],
        temperature=0,
        max_tokens=5,
    )
    result = response.choices[0].message.content.strip().upper()
    return "CAPTURE" if "CAPTURE" in result else "QUERY"
