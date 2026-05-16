---
tags: [arquitectura, agentes, pipeline, responsabilidades]
---

# Arquitectura de agentes

Los agentes son la capa de lógica de negocio del proyecto. Cada uno tiene una responsabilidad única y expone un método `run()`. Los servicios son los proveedores técnicos; los agentes son los orquestadores de negocio.

## Diferencia: agente vs servicio

| Concepto | Responsabilidad | Ejemplo |
|----------|----------------|---------|
| Servicio | Hacer una operación técnica | `OpenAITranscriptionService.transcribe()` |
| Agente | Aplicar reglas de negocio usando servicios | `TasksAgent` decide qué tareas crear |

Un `TasksAgent` sabe que "si el texto dice 'requiere revisión', no crear tarea". El servicio solo sabe hacer la llamada HTTP a Google.

## Mapa de agentes del proyecto

```
agents/
├── transcription_agent.py   → envuelve TranscriptionService
├── analysis_agent.py        → carga prompt, envuelve AnalysisService
├── markdown_agent.py        → genera .md de respaldo en output/
├── knowledge_base_agent.py  → enruta el resultado a Knowledge_Base/
├── tasks_agent.py           → aplica reglas y crea Google Tasks
├── calendar_agent.py        → aplica reglas y crea eventos de Calendar
├── archive_agent.py         → mueve el MP3 a processed/
└── drive_agent.py           → descarga de Drive, sube KB, mueve a Processed
```

## Estructura típica de un agente

```python
class ArchiveAgent:
    def __init__(self, processed_dir: Path):
        self.processed_dir = processed_dir

    def run(self, mp3_path: Path) -> None:
        destination = self.processed_dir / mp3_path.name
        if destination.exists():
            ts = datetime.now().strftime("%H%M%S")
            destination = self.processed_dir / f"{mp3_path.stem}_{ts}.mp3"
        shutil.move(str(mp3_path), str(destination))
        print(f"[ArchiveAgent] Moved to: {destination}")
```

Patrón consistente:
1. `__init__` recibe dependencias
2. `run()` es la única interfaz pública
3. Métodos privados con `_` para detalles internos

## Agentes opcionales

TasksAgent, CalendarAgent y DriveAgent son opcionales. Se crean solo si existen credenciales de Google:

```python
tasks_agent = (
    TasksAgent(tasks_svc, kb_dir / "Tasks" / "created_tasks.json")
    if tasks_svc else None
)
```

Los nodos de LangGraph verifican si el agente existe antes de ejecutar:

```python
def node(state: PipelineState) -> dict:
    if not agent:
        return {}
    ...
```

## Conceptos relacionados

- [[20_arquitectura_servicios]] — la capa debajo de los agentes
- [[29_langgraph_intro]] — cómo los agentes se convierten en nodos de un grafo
- [[31_langgraph_pipeline]] — el pipeline completo con todos los agentes
