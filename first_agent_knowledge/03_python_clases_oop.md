---
tags: [python, fundamentos, clases, oop]
---

# Clases y programación orientada a objetos en Python

Las clases agrupan datos (atributos) y comportamiento (métodos) en una sola unidad. En este proyecto, cada agente es una clase con un método `run()`.

## Definición básica

```python
class ArchiveAgent:
    def __init__(self, processed_dir: Path):
        self.processed_dir = processed_dir   # atributo de instancia
        processed_dir.mkdir(parents=True, exist_ok=True)

    def run(self, mp3_path: Path) -> None:
        destination = self.processed_dir / mp3_path.name
        shutil.move(str(mp3_path), str(destination))
```

`__init__` es el constructor — se ejecuta cuando haces `ArchiveAgent(processed_dir)`.  
`self` es la referencia al objeto actual (como `this` en otros lenguajes).

## Herencia y clases base abstractas

Para que los servicios sean intercambiables, se define una interfaz base.

```python
from abc import ABC, abstractmethod

class TranscriptionService(ABC):
    @abstractmethod
    def transcribe(self, audio_path: Path) -> str:
        ...
```

`ABC` = Abstract Base Class. Marca el contrato que deben cumplir las subclases.

```python
class OpenAITranscriptionService(TranscriptionService):
    def __init__(self, client, model: str = "whisper-1"):
        self.client = client
        self.model  = model

    def transcribe(self, audio_path: Path) -> str:
        with open(audio_path, "rb") as f:
            response = self.client.audio.transcriptions.create(
                model=self.model, file=f
            )
        return response.text
```

La subclase implementa `transcribe()`. Si no lo hace, Python lanza `TypeError`.

## Métodos privados (convención)

Un método que empieza con `_` es privado por convención — indica "uso interno".

```python
class TasksAgent:
    def run(self, result, source):         # público — interfaz externa
        for task in result.tasks:
            self._create_if_new(task, source)

    def _create_if_new(self, title, source):  # privado — detalle interno
        h = self._task_hash(source, title)
        ...

    def _task_hash(self, source, title) -> str:
        return hashlib.sha256(f"{source}:{title}".lower().encode()).hexdigest()[:16]
```

## Conceptos relacionados

- [[20_arquitectura_servicios]] — cómo las clases base hacen el código intercambiable
- [[21_arquitectura_agentes]] — estructura de cada agente del proyecto
- [[07_python_dataclasses_typeddict]] — clases simplificadas para datos puros
