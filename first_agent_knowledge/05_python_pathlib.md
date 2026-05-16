---
tags: [python, fundamentos, archivos, pathlib]
---

# Manejo de archivos con pathlib

`pathlib.Path` es la forma moderna de trabajar con rutas y archivos en Python. Es multiplataforma: funciona igual en Windows, Mac y Linux.

## Crear rutas

```python
from pathlib import Path

# Desde una cadena
input_dir = Path("input")
output_dir = Path("output")

# Combinando partes con /
kb_dir = Path("Knowledge_Base")
ideas_file = kb_dir / "Ideas" / "ideas.md"
# resultado: Knowledge_Base/Ideas/ideas.md
```

## Verificar existencia y crear carpetas

```python
# Verificar si existe
if ideas_file.exists():
    print("El archivo existe")

# Crear carpeta (y todas las intermedias)
(kb_dir / "Ideas").mkdir(parents=True, exist_ok=True)
# parents=True → crea carpetas intermedias
# exist_ok=True → no falla si ya existe
```

## Leer y escribir archivos

```python
# Leer texto
contenido = ideas_file.read_text(encoding="utf-8")

# Escribir texto (reemplaza el archivo completo)
ideas_file.write_text("# Ideas\n\nPrimera idea", encoding="utf-8")
```

## Propiedades útiles

```python
path = Path("input/reunion_boya.mp3")

path.name      # "reunion_boya.mp3"
path.stem      # "reunion_boya"
path.suffix    # ".mp3"
path.parent    # Path("input")
path.exists()  # True / False
path.is_file() # True
path.is_dir()  # False
```

## Uso real en el proyecto

```python
# En file_service.py — buscar todos los MP3
def find_all_mp3(input_dir: Path) -> list[Path]:
    return sorted(input_dir.glob("*.mp3"))

# En knowledge_base_agent.py — construir ruta del archivo de salida
def _make_filename(self, title: str) -> str:
    today = date.today().isoformat()
    safe  = re.sub(r"[^\w\s-]", "", title.lower())
    safe  = re.sub(r"\s+", "_", safe.strip())[:50]
    return f"{today}_{safe}.md"

target = self.kb_dir / "Meetings" / self._make_filename(result.title)
```

## Mover archivos con shutil

`pathlib` solo crea/lee/escribe rutas. Para mover archivos se usa `shutil`:

```python
import shutil

shutil.move(str(mp3_path), str(destination))
```

## Conceptos relacionados

- [[06_python_errores]] — qué hacer si el archivo no existe
- [[25_knowledge_base]] — estructura de carpetas de la Knowledge Base
- [[21_arquitectura_agentes]] — ArchiveAgent usa shutil para mover MP3
