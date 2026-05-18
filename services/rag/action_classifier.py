from openai import OpenAI

_SYSTEM = """El usuario quiere ejecutar una acción. Clasifícala como:

- COMPLETE_TASK: quiere marcar una tarea como completada o hecha.
  Ejemplos: "marca como completada la tarea X", "ya hice X", "completa la tarea de Y".

- ARCHIVE_EVENTS: quiere archivar o borrar eventos/citas pasados del calendario.
  Ejemplos: "archiva los eventos pasados", "borra las citas de la semana pasada",
  "limpia el calendario".

Responde ÚNICAMENTE con una de estas palabras: COMPLETE_TASK o ARCHIVE_EVENTS, sin explicación."""


def classify_action(client: OpenAI, message: str) -> str:
    """Level-2 classifier for ACTION intents. Returns 'COMPLETE_TASK' or 'ARCHIVE_EVENTS'."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _SYSTEM},
            {"role": "user",   "content": message},
        ],
        temperature=0,
        max_tokens=10,
    )
    result = response.choices[0].message.content.strip().upper()
    if "COMPLETE_TASK" in result:
        return "COMPLETE_TASK"
    return "ARCHIVE_EVENTS"
