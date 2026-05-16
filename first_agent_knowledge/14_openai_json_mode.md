---
tags: [openai, json, parsing, response-format]
---

# JSON mode en OpenAI — response_format

Por defecto, GPT responde en texto libre. `response_format={"type": "json_object"}` fuerza al modelo a devolver siempre un JSON válido, parseable directamente con `json.loads()`.

## El problema que resuelve

Sin JSON mode, GPT puede devolver:

```
La reunión tuvo 3 participantes. Las tareas identificadas son:
1. Revisar el contrato
2. Enviar el resumen

Tags: #reunion, #boya
```

Parsear esto con código es frágil: cualquier variación en el formato rompe el parser.

## Con JSON mode

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[...],
    response_format={"type": "json_object"}  # ← fuerza JSON válido
)
```

El modelo devuelve:

```json
{
  "category": "Reunión",
  "title": "Revisión del proyecto BOYA",
  "tasks": ["Revisar el contrato", "Enviar el resumen"],
  "tags": ["#reunion", "#boya"],
  "participants": ["Oscar", "Ana"],
  "decisions": []
}
```

## Parsing del JSON en Python

```python
import json

raw = response.choices[0].message.content
data = json.loads(raw)  # dict de Python

result = AnalysisResult(
    category=data.get("category", "Nota general"),
    title=data.get("title", "Sin título"),
    tasks=data.get("tasks", []),
    tags=data.get("tags", []),
    ...
)
```

Se usa `.get("campo", valor_default)` para que un campo faltante no rompa el código.

## Regla importante: el prompt debe pedir JSON

Cuando se usa `response_format=json_object`, el system prompt **debe** mencionar que la respuesta debe ser JSON. Si no, la API lanza un error.

```markdown
# En prompts/analysis_agent.md:
Responde SIEMPRE con un JSON válido con la siguiente estructura:
{
  "category": "...",
  "title": "...",
  ...
}
```

## Conceptos relacionados

- [[13_openai_gpt4o_mini]] — la llamada completa al modelo
- [[22_prompts_markdown]] — el system prompt que define el schema JSON
- [[23_analysis_result]] — la dataclass que se construye desde el JSON
