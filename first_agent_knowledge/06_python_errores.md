---
tags: [python, fundamentos, errores, excepciones]
---

# Manejo de errores en Python

Los errores en Python se manejan con `try/except`. En este proyecto, el manejo de errores es crítico: si un MP3 falla, el archivo no debe moverse y el sistema debe continuar con el siguiente.

## Estructura básica

```python
try:
    resultado = agente.run(mp3_path)
except Exception as e:
    print(f"Error procesando {mp3_path.name}: {e}")
```

## Capturar tipos específicos de errores

```python
try:
    contenido = archivo.read_text(encoding="utf-8")
except FileNotFoundError:
    print("El archivo no existe")
except PermissionError:
    print("Sin permisos para leer el archivo")
except Exception as e:
    print(f"Error inesperado: {e}")
```

## Usar raise para relanzar

```python
def load_prompt(prompts_dir: Path, filename: str) -> str:
    path = prompts_dir / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Prompt no encontrado: {path}\n"
            f"Archivos disponibles: {list(prompts_dir.glob('*.md'))}"
        )
    return path.read_text(encoding="utf-8")
```

## Patrón en los nodos de LangGraph

Cada nodo del pipeline captura errores y los comunica a través del estado:

```python
def make_transcription_node(agents: dict, dirs: dict):
    agent = agents["transcription"]

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}           # error previo — saltamos este nodo
        try:
            transcript = agent.run(state["mp3_path"])
            return {"transcript": transcript}
        except Exception as e:
            return {"error": f"[transcription] {e}"}  # propagamos el error

    return node
```

Si un nodo devuelve `{"error": "..."}`, todos los nodos siguientes hacen early return `{}`. El MP3 nunca se mueve a `processed/`.

## Diferencia entre error fatal y warning

Los nodos opcionales (Drive, Tasks, Calendar) usan `print` en lugar de propagar el error. Un fallo en Google Drive no debe detener el pipeline principal.

```python
except Exception as e:
    print(f"[DriveAgent] Sync warning: {e}")
    return {}   # continúa el pipeline
```

Los nodos obligatorios (transcripción, análisis) sí propagan el error con `{"error": ...}`.

## Conceptos relacionados

- [[28_manejo_errores_pipeline]] — cómo el error se propaga entre nodos
- [[31_langgraph_pipeline]] — implementación real del pipeline con errores
- [[02_python_funciones]] — los try/except viven dentro de funciones
