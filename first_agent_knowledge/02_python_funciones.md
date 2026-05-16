---
tags: [python, fundamentos, funciones]
---

# Funciones en Python

Una función encapsula un bloque de lógica reutilizable. En este proyecto, cada agente expone su lógica principal en un método `run()`.

## Definición básica

```python
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"

resultado = saludar("Oscar")  # "Hola, Oscar"
```

## Parámetros opcionales (default args)

```python
def crear_task(titulo: str, due_days: int = 7) -> None:
    print(f"Creando tarea: {titulo} — vence en {due_days} días")

crear_task("Revisar contrato")         # usa default: 7 días
crear_task("Llamar al cliente", due_days=1)  # sobreescribe
```

## Retornar múltiples valores

Python permite retornar una tupla implícita. Se usa en el pipeline para comunicar éxito y error.

```python
def procesar(mp3_path: Path) -> tuple[bool, str]:
    try:
        # ... lógica ...
        return True, ""
    except Exception as e:
        return False, str(e)

ok, error_msg = procesar(Path("input/audio.mp3"))
```

## Parámetros con tipo Optional

```python
from typing import Optional
from datetime import date

def create_task(title: str, due_date: Optional[date] = None) -> str:
    # si due_date es None, la tarea no tiene fecha límite
    ...
```

## Funciones como parámetro (callbacks)

En LangGraph, los nodos son funciones que se pasan como argumento al grafo.

```python
def make_transcription_node(agents: dict, dirs: dict):
    agent = agents["transcription"]

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        transcript = agent.run(state["mp3_path"])
        return {"transcript": transcript}

    return node  # retorna la función sin ejecutarla
```

## Conceptos relacionados

- [[03_python_clases_oop]] — métodos son funciones dentro de clases
- [[06_python_errores]] — manejo de errores dentro de funciones
- [[30_langgraph_stategraph]] — los nodos de LangGraph son funciones
