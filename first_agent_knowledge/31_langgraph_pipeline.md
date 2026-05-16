---
tags: [langgraph, pipeline, nodos, implementacion, grafo]
---

# El pipeline LangGraph del proyecto — 9 nodos

El pipeline completo tiene 9 nodos en secuencia lineal. Los nodos opcionales (Drive, Tasks, Calendar) se saltan si el agente no está configurado.

## El grafo completo

```
transcription_node
        |
analysis_node
        |
markdown_node
        |
knowledge_base_node
        |
drive_sync_node  (opcional — solo si Drive está configurado)
        |
tasks_node       (opcional — solo si credenciales Google existen)
        |
calendar_node    (opcional — solo si credenciales Google existen)
        |
archive_node
        |
drive_processed_node  (opcional)
        |
       END
```

## Los 9 nodos y su responsabilidad

| Nodo | Agente | Qué hace | Campos que actualiza |
|------|--------|----------|---------------------|
| `transcription_node` | `TranscriptionAgent` | Convierte MP3 en texto | `transcript` |
| `analysis_node` | `AnalysisAgent` | Clasifica y extrae datos del texto | `result` |
| `markdown_node` | `MarkdownAgent` | Guarda respaldo `.md` en `output/` | — |
| `knowledge_base_node` | `KnowledgeBaseAgent` | Enruta a KB según categoría | — |
| `drive_sync_node` | `DriveAgent` (upload) | Sube archivos KB a Drive | — |
| `tasks_node` | `TasksAgent` | Crea Google Tasks si aplica | — |
| `calendar_node` | `CalendarAgent` | Crea Google Calendar events si aplica | — |
| `archive_node` | `ArchiveAgent` | Mueve MP3 a `processed/` | — |
| `drive_processed_node` | `DriveAgent` (move) | Mueve MP3 en Drive a Processed | — |

## Construcción en graph.py

```python
def build_graph(agents: dict, dirs: dict):
    graph = StateGraph(PipelineState)

    graph.add_node("transcription",    make_transcription_node(agents, dirs))
    graph.add_node("analysis",         make_analysis_node(agents))
    graph.add_node("markdown",         make_markdown_node(agents, dirs))
    graph.add_node("knowledge_base",   make_kb_node(agents))
    graph.add_node("drive_sync",       make_drive_sync_node(agents))
    graph.add_node("tasks",            make_tasks_node(agents))
    graph.add_node("calendar",         make_calendar_node(agents))
    graph.add_node("archive",          make_archive_node(agents))
    graph.add_node("drive_processed",  make_drive_processed_node(agents))

    graph.set_entry_point("transcription")

    sequence = [
        ("transcription",   "analysis"),
        ("analysis",        "markdown"),
        ("markdown",        "knowledge_base"),
        ("knowledge_base",  "drive_sync"),
        ("drive_sync",      "tasks"),
        ("tasks",           "calendar"),
        ("calendar",        "archive"),
        ("archive",         "drive_processed"),
        ("drive_processed", END),
    ]
    for src, dst in sequence:
        graph.add_edge(src, dst)

    return graph.compile()
```

## Cómo los agentes llegan al grafo

El `OrchestratorAgent` construye todos los agentes y los pasa al grafo en un diccionario:

```python
self.pipeline = build_graph(
    agents={
        "transcription":  transcription_agent,
        "analysis":       analysis_agent,
        "markdown":       markdown_agent,
        "kb":             kb_agent,
        "tasks":          tasks_agent,       # puede ser None
        "calendar":       calendar_agent,    # puede ser None
        "archive":        archive_agent,
        "drive":          drive_agent,       # puede ser None
        "drive_sync_fn":  self._sync_kb_to_drive if drive_agent else None,
    },
    dirs={"output": output_dir, "kb": kb_dir},
)
```

## Invocación por archivo

Para cada MP3, el orchestrator invoca el grafo con el estado inicial:

```python
def _process_one(self, mp3_path: Path) -> bool:
    initial_state = {
        "mp3_path": mp3_path, "mp3_name": mp3_path.name,
        "mp3_stem": mp3_path.stem,
        "transcript": "", "result": None, "error": None,
    }
    final_state = self.pipeline.invoke(initial_state)
    return not final_state.get("error")
```

## Conceptos relacionados

- [[29_langgraph_intro]] — por qué se usó LangGraph
- [[30_langgraph_stategraph]] — los conceptos de StateGraph, nodos y edges
- [[28_manejo_errores_pipeline]] — cómo el error detiene el grafo
- [[21_arquitectura_agentes]] — los agentes que envuelven cada nodo
