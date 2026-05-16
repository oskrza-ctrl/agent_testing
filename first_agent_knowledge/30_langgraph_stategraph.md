---
tags: [langgraph, stategraph, nodos, edges, estado, typeddict]
---

# LangGraph — StateGraph, nodos y edges

`StateGraph` es la clase principal de LangGraph. Define el grafo, sus nodos, las conexiones entre ellos y el estado que comparten.

## Conceptos clave

### Estado (State)
Un `TypedDict` que fluye entre todos los nodos. Cada nodo puede leer cualquier campo del estado y devolver un diccionario con los campos que actualiza. LangGraph hace el merge automáticamente.

```python
class PipelineState(TypedDict):
    mp3_path:   Any           # leído por transcription_node
    transcript: str           # escrito por transcription_node, leído por analysis_node
    result:     Any           # escrito por analysis_node, leído por todos los siguientes
    error:      Optional[str] # escrito por cualquier nodo que falle
```

### Nodo (Node)
Una función que recibe el estado completo y devuelve un dict parcial con solo los campos que cambia:

```python
def make_analysis_node(agents: dict):
    agent = agents["analysis"]

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}                         # ← devuelve dict vacío (sin cambios)
        try:
            result = agent.run(state["transcript"])
            return {"result": result}          # ← solo el campo que cambió
        except Exception as e:
            return {"error": f"[analysis] {e}"}

    return node   # ← factory pattern: devuelve la función, no la ejecuta
```

### Edge
Una conexión entre dos nodos. En el proyecto son todos lineales (un camino, sin bifurcaciones).

```python
graph.add_edge("transcription", "analysis")   # después de transcription, va a analysis
```

### Entry point
El primer nodo que ejecuta LangGraph:

```python
graph.set_entry_point("transcription")
```

### END
Un marcador especial que indica el fin del grafo:

```python
from langgraph.graph import StateGraph, END
graph.add_edge("drive_processed", END)
```

## Construcción y compilación

```python
from langgraph.graph import StateGraph, END
from pipeline.state import PipelineState

graph = StateGraph(PipelineState)

# Agregar nodos
graph.add_node("transcription", make_transcription_node(agents, dirs))
graph.add_node("analysis",      make_analysis_node(agents))

# Conectar nodos
graph.add_edge("transcription", "analysis")
graph.add_edge("analysis", END)

# Punto de entrada
graph.set_entry_point("transcription")

# Compilar — a partir de aquí es inmutable
pipeline = graph.compile()
```

## Invocar el grafo

```python
initial_state = {
    "mp3_path":   Path("input/audio.mp3"),
    "mp3_name":   "audio.mp3",
    "mp3_stem":   "audio",
    "transcript": "",
    "result":     None,
    "error":      None,
}

final_state = pipeline.invoke(initial_state)
# final_state contiene el estado completo después de todos los nodos
```

## Factory pattern — por qué los nodos son funciones que retornan funciones

Los nodos necesitan acceso a los agentes y directorios, pero LangGraph solo acepta funciones `(state) -> dict`. La solución es un factory:

```python
def make_transcription_node(agents: dict, dirs: dict):
    # Captura agents y dirs en el closure
    agent = agents["transcription"]
    output_dir = dirs["output"]

    def node(state: PipelineState) -> dict:
        # Aquí tiene acceso a agent y output_dir
        transcript = agent.run(state["mp3_path"])
        return {"transcript": transcript}

    return node   # retorna la función lista para ser nodo
```

## Conceptos relacionados

- [[29_langgraph_intro]] — por qué LangGraph reemplaza el código imperativo
- [[31_langgraph_pipeline]] — el grafo real de 9 nodos
- [[07_python_dataclasses_typeddict]] — TypedDict que define el estado
- [[02_python_funciones]] — closures y funciones como argumentos
