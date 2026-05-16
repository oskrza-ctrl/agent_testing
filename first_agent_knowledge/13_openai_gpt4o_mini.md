---
tags: [openai, gpt4o-mini, analisis, prompts, llm]
---

# Análisis de texto con GPT-4o-mini

GPT-4o-mini recibe el transcript y lo clasifica en una de 6 categorías, extrae tareas, ideas, recordatorios y genera un JSON estructurado.

## Por qué GPT-4o-mini

- Costo: ~$0.15 / millón de tokens de entrada (vs $2.50 de GPT-4o)
- Calidad: suficiente para clasificación y resumen de notas personales
- Velocidad: más rápido que GPT-4o

## La llamada a la API

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user",   "content": transcript}
    ],
    response_format={"type": "json_object"},
    temperature=0.3   # bajo para respuestas consistentes
)

raw_json = response.choices[0].message.content
data = json.loads(raw_json)
```

## El rol del system prompt

El system prompt es el conjunto de instrucciones que le dice al modelo cómo comportarse. En el proyecto se carga desde `prompts/analysis_agent.md`.

El prompt define:
- Las 6 categorías y sus criterios
- Los campos del JSON de salida (15 campos)
- La regla de NO inventar fechas absolutas
- Los tags de fallback si no hay tags específicos

## Temperature

`temperature` controla la aleatoriedad de la respuesta:
- `0.0` → siempre la misma respuesta (determinista)
- `1.0` → creativo, variable
- `0.3` → equilibrio entre consistencia y naturalidad (valor usado en el proyecto)

Para clasificación y extracción de datos se prefiere temperature baja.

## Tokens en el contexto de análisis

Un transcript de 5 minutos tiene ~750 palabras ≈ ~1,000 tokens.
El system prompt del proyecto tiene ~800 tokens.
Total por request: ~1,800 tokens de entrada.

Con 1,000 audios procesados: 1,800,000 tokens = $0.27 USD en total.

## Conceptos relacionados

- [[14_openai_json_mode]] — por qué se pide JSON y cómo se parsea
- [[22_prompts_markdown]] — cómo se carga el prompt desde un archivo .md
- [[23_analysis_result]] — la estructura del JSON de salida
- [[24_categorias_contenido]] — las 6 categorías que el modelo clasifica
