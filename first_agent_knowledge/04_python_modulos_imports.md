---
tags: [python, fundamentos, modulos, imports]
---

# Módulos e imports en Python

Un módulo es un archivo `.py`. Un paquete es una carpeta con un `__init__.py`. Los imports permiten usar código de otros archivos.

## Import básico

```python
import os
import hashlib
import json
from pathlib import Path
from datetime import date, timedelta
```

## Import desde un paquete del proyecto

```python
# Desde services/analysis/analysis_result.py
from services.analysis.analysis_result import AnalysisResult

# Desde agents/transcription_agent.py
from agents.transcription_agent import TranscriptionAgent

# Desde pipeline/state.py
from pipeline.state import PipelineState
```

La ruta del import sigue la estructura de carpetas: `services.analysis.analysis_result`.

## __init__.py

Un archivo `__init__.py` (puede estar vacío) convierte una carpeta en un paquete Python. Sin él, los imports fallan.

```
pipeline/
├── __init__.py     ← necesario para que funcione "from pipeline.graph import build_graph"
├── graph.py
├── nodes.py
└── state.py
```

## Imports opcionales (solo si existe)

Para integraciones opcionales como Google Drive, se importa dentro de la función y se captura el error si no está instalado.

```python
# En agents/drive_agent.py
from services.drive.google_drive_service import GoogleDriveService
```

Si el módulo no está, el import falla al arrancar. Por eso las credenciales se verifican antes de instanciar el servicio.

## Imports circulares — cómo evitarlos

Si `agents/orchestrator_agent.py` importa de `agents/knowledge_base_agent.py` y viceversa, hay un import circular. La solución es importar solo lo que se necesita, y mover imports pesados al interior de funciones cuando sea necesario.

```python
# En orchestrator_agent.py — import local para evitar circular
def _sync_kb_to_drive(self, result) -> None:
    from agents.knowledge_base_agent import ACCUMULATIVE, INDIVIDUAL  # import local
    ...
```

## Conceptos relacionados

- [[03_python_clases_oop]] — las clases se importan desde sus módulos
- [[20_arquitectura_servicios]] — cómo se organiza la jerarquía de módulos
- [[21_arquitectura_agentes]] — cada agente vive en su propio módulo
