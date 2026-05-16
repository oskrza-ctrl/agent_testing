---
tags: [python, fundamentos, configuracion, dotenv, seguridad]
---

# Variables de entorno y .env

Las API keys y configuraciones sensibles nunca deben estar en el código fuente. Se guardan en un archivo `.env` que nunca se sube a git.

## El problema que resuelve

Si pones tu API key directamente en el código:

```python
client = openai.OpenAI(api_key="sk-proj-...")  # NUNCA hacer esto
```

Cualquier persona que vea el repositorio en GitHub puede ver tu clave y usarla a tu costo.

## Solución: archivo .env

```
# .env  (nunca subir a git)
OPENAI_API_KEY=sk-proj-8tNGuPtvnaiRr93BYiM16...
GOOGLE_DRIVE_INBOX_FOLDER_ID=1pgehcCoulbemk_c1XmF1...
GOOGLE_DRIVE_PROCESSED_FOLDER_ID=1a0xbNnV4R19Fv6LZ...
GOOGLE_DRIVE_KB_FOLDER_ID=1rtYFbFItvoZrI1V0xN01...
```

## Leer variables en Python

```python
import os
from dotenv import load_dotenv

load_dotenv()  # carga el archivo .env al entorno del proceso

api_key = os.getenv("OPENAI_API_KEY")
inbox_id = os.getenv("GOOGLE_DRIVE_INBOX_FOLDER_ID")  # None si no está definida
```

`os.getenv()` devuelve `None` si la variable no existe. Se puede pasar un default:

```python
timezone = os.getenv("GOOGLE_CALENDAR_TIMEZONE", "America/Mexico_City")
```

## .gitignore — excluir .env de git

```
# .gitignore
.env
credentials/
__pycache__/
*.pyc
.venv/
```

## .env.example — documentar variables sin exponer valores

Se sube al repo como referencia para otros desarrolladores:

```
# .env.example
OPENAI_API_KEY=tu_api_key_aqui
GOOGLE_DRIVE_INBOX_FOLDER_ID=id_de_tu_carpeta_inbox
GOOGLE_DRIVE_PROCESSED_FOLDER_ID=id_de_tu_carpeta_processed
GOOGLE_DRIVE_KB_FOLDER_ID=id_de_tu_carpeta_knowledge_base
GOOGLE_CALENDAR_TIMEZONE=America/Mexico_City
```

## Uso real en main.py

```python
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY no configurada en .env")

client = openai.OpenAI(api_key=api_key)
```

## Conceptos relacionados

- [[10_autenticacion_apis]] — diferencia entre API key y OAuth2
- [[15_google_apis_overview]] — cómo se configuran las credenciales de Google
- [[33_vision_second_brain]] — arquitectura general del proyecto
