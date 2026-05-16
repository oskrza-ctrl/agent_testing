---
tags: [langgraph, orchestracion, grafo, pipeline, agentes]
---

# LangGraph — qué es y por qué usarlo

LangGraph es una librería de Python que permite definir flujos de trabajo como grafos formales. En lugar de una secuencia de llamadas imperativas en el código, se declara explícitamente qué nodos existen y cómo están conectados.

## El problema que resuelve

**Antes de LangGraph** — código imperativo en `_process_one()`:

```python
def _process_one(self, mp3_path: Path) -> bool:
    transcript = self.transcription_agent.run(mp3_path)
    if not transcript:
        return False
    result = self.analysis_agent.run(transcript)
    if not result:
        return False
    self.markdown_agent.run(...)
    self.kb_agent.run(result, mp3_path.name)
    if self.tasks_agent:
        self.tasks_agent.run(result, mp3_path.name)
    if self.calendar_agent:
        self.calendar_agent.run(result, mp3_path.name)
    self.archive_agent.run(mp3_path)
    return True
```

Problemas:
- El manejo de errores está mezclado con la lógica
- Agregar un nodo requiere modificar `_process_one()`
- Difícil de visualizar, difícil de extender

## Con LangGraph — grafo declarativo

```python
graph = StateGraph(PipelineState)

graph.add_node("transcription", transcription_node)
graph.add_node("analysis",      analysis_node)
graph.add_node("archive",       archive_node)

graph.add_edge("transcription", "analysis")
graph.add_edge("analysis", "archive")

graph.set_entry_point("transcription")
pipeline = graph.compile()

# Invocar
final_state = pipeline.invoke({"mp3_path": path, ...})
```

El flujo está declarado, no codificado. Agregar un nodo = `add_node()` + `add_edge()`.

## Estado compartido — PipelineState

Todos los nodos leen y escriben en el mismo estado. Un nodo actualiza el transcript, el siguiente lo lee. No se pasan parámetros entre nodos — todo fluye por el estado.

```python
class PipelineState(TypedDict):
    mp3_path:   Any
    transcript: str
    result:     Any
    error:      Optional[str]
```

## Capacidades futuras

LangGraph también soporta:
- **Grafos condicionales** — distintos caminos según el resultado de un nodo
- **Paralelización** — ejecutar múltiples nodos en paralelo (ej: Tasks y Calendar simultáneamente)
- **Checkpointing** — guardar el estado en disco para reanudar si el proceso se interrumpe
- **Human-in-the-loop** — pausar el grafo para aprobación manual

El proyecto usa un grafo lineal simple ahora, pero la arquitectura está lista para estas extensiones.

## Conceptos relacionados

- [[30_langgraph_stategraph]] — los conceptos técnicos de StateGraph
- [[31_langgraph_pipeline]] — el pipeline real de 9 nodos
- [[21_arquitectura_agentes]] — los agentes que se convierten en nodos
