from openai import OpenAI

_SYSTEM = """Clasifica el mensaje del usuario como:

- PIPELINE: el usuario quiere procesar audios, correr el pipeline, revisar el inbox
  o ejecutar el sistema de procesamiento. Ejemplos: "procesa los audios",
  "corre el pipeline", "revisa el inbox", "hay audios nuevos?", "procesar".

- CAPTURE: el usuario está compartiendo información nueva — una idea, tarea, recordatorio,
  nota de reunión, proyecto o cualquier contenido que debe guardarse en su base de conocimiento.

- QUERY: el usuario está haciendo una pregunta, buscando información o pidiendo un resumen
  de algo que ya está en su base de conocimiento.

Responde ÚNICAMENTE con una de estas palabras: PIPELINE, CAPTURE o QUERY, sin explicación."""


def classify_intent(client: OpenAI, message: str) -> str:
    """Returns 'PIPELINE', 'CAPTURE' or 'QUERY'."""
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
    if "PIPELINE" in result:
        return "PIPELINE"
    if "CAPTURE" in result:
        return "CAPTURE"
    return "QUERY"
