---
tags: [errores, pipeline, langgraph, resiliencia, early-return]
---

# Manejo de errores en el pipeline

El pipeline tiene un contrato claro: si algo falla, el MP3 original NO se mueve. El archivo queda en `input/` para revisión manual y reintento. Ningún error parcial debe dejar el sistema en un estado inconsistente.

## El patrón: error en el estado

LangGraph usa un estado compartido (`PipelineState`). Cuando un nodo falla, escribe el error en el estado:

```python
def node(state: PipelineState) -> dict:
    try:
        result = agent.run(state["mp3_path"])
        return {"result": result}
    except Exception as e:
        return {"error": f"[analysis] {e}"}
```

## Early return en nodos siguientes

Todos los nodos (excepto los opcionales con warnings) verifican el error al inicio:

```python
def node(state: PipelineState) -> dict:
    if state.get("error"):
        return {}   # saltamos sin hacer nada
    ...
```

Si el nodo de transcripción falla → escribe `{"error": "..."}` → todos los nodos siguientes hacen early return `{}` → el nodo `archive_node` también hace early return → el MP3 NO se mueve.

## Flujo con error

```
transcription_node  → {"error": "[transcription] file not found"}
analysis_node       → {} (early return, ve el error)
markdown_node       → {} (early return)
knowledge_base_node → {} (early return)
drive_sync_node     → {} (early return)
tasks_node          → {} (early return)
calendar_node       → {} (early return)
archive_node        → {} (early return — MP3 queda en input/)
drive_processed_node → {} (early return)
```

## Errores fatales vs warnings

No todos los errores deben detener el pipeline.

**Error fatal** (propaga `{"error": ...}`):
- Transcripción fallida — sin transcript no hay nada que procesar
- Análisis fallido — sin resultado no hay datos para guardar

**Warning** (solo `print`, continúa el pipeline):
- Drive sync fallida — la KB local ya está guardada
- Google Tasks fallida — el pipeline principal no depende de Tasks
- Google Calendar fallida — igual

```python
# Nodo opcional con warning
def node(state: PipelineState) -> dict:
    if state.get("error"):
        return {}
    agent = agents.get("tasks")
    if not agent:
        return {}
    try:
        agent.run(state["result"], state["mp3_name"])
        return {}
    except Exception as e:
        print(f"[TasksAgent] Warning: {e}")   # no propaga el error
        return {}
```

## Resumen en el OrchestratorAgent

Al final, el orchestrator verifica el estado final y reporta:

```python
final_state = self.pipeline.invoke(initial_state)

if final_state.get("error"):
    print(f"[OrchestratorAgent] ERROR on {mp3_path.name}: {final_state['error']}")
    print("[OrchestratorAgent] File was NOT moved. Check input/ for the original.")
    return False

return True
```

Al terminar todos los archivos se imprime el resumen:
```
Done. Total: 3 | OK: 2 | Failed: 1
```

## Conceptos relacionados

- [[06_python_errores]] — try/except en Python
- [[30_langgraph_stategraph]] — cómo el estado fluye entre nodos
- [[31_langgraph_pipeline]] — los 9 nodos reales y su manejo de errores
