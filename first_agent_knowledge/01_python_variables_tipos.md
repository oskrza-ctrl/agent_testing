---
tags: [python, fundamentos, variables]
---

# Variables y tipos de datos en Python

Python es un lenguaje de tipado dinámico: no declaras el tipo de una variable, Python lo infiere en tiempo de ejecución. Aun así, es buena práctica usar [[07_python_dataclasses_typeddict|type hints]] para documentar intenciones.

## Tipos básicos

```python
# Texto
nombre = "Second Brain Agent"
categoria = "Reunión"

# Números
costo_por_minuto = 0.006   # float
tokens_entrada = 150000    # int

# Booleano
drive_habilitado = True
tasks_habilitado = False

# None — ausencia de valor
error = None
resultado = None
```

## Listas

Las listas almacenan colecciones ordenadas. En el proyecto se usan para ideas, tareas y recordatorios.

```python
ideas = ["Automatizar el inbox", "Agregar soporte para texto"]
tasks = ["Revisar el contrato [candidato: Google Tasks]"]
tags  = ["#proyecto", "#reunion", "#accion"]

# Agregar un elemento
ideas.append("Usar Whisper local en el futuro")

# Recorrer
for idea in ideas:
    print(idea)
```

## Diccionarios

Los diccionarios almacenan pares clave-valor. Se usan para parsear respuestas JSON de OpenAI.

```python
entry = {
    "hash":           "a1b2c3d4",
    "source":         "reunion_boya.mp3",
    "task_text":      "[BOYA] Revisar contrato",
    "google_task_id": "abc123",
    "created_at":     "2026-05-15",
}

# Acceder a un campo
print(entry["task_text"])

# Verificar si existe una clave
if "error" in entry:
    print("Algo falló")
```

## Strings — operaciones comunes

```python
texto = "  Hola mundo  "

texto.strip()           # "Hola mundo"
texto.lower()           # "  hola mundo  "
texto.startswith("Ho")  # True
texto[:50]              # primeros 50 caracteres
f"Archivo: {nombre}"    # f-string (interpolación)
```

## Conceptos relacionados

- [[02_python_funciones]] — cómo usar estas variables en funciones
- [[07_python_dataclasses_typeddict]] — estructuras de datos más complejas
- [[14_openai_json_mode]] — parsear dicts devueltos por OpenAI
