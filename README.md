# Agent Testing

Pipeline local de IA: **MP3 → transcripción → análisis → Markdown**.

## Objetivo

Validar el flujo completo de manera local:

1. Tomar un archivo MP3 desde `input/`
2. Transcribirlo usando una API de IA
3. Analizar el transcript con un modelo de lenguaje
4. Generar un archivo Markdown en `output/`

## Estructura

```
agent_testing/
├── input/       # Coloca aquí tu archivo MP3
├── output/      # Aquí aparece el Markdown generado
├── services/    # Módulos de integración con APIs (transcripción, análisis)
├── prompts/     # Prompts de IA reutilizables
├── main.py      # Entry point del pipeline
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

```bash
# 1. Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
copy .env.example .env
# Edita .env y agrega tu API key
```

## Uso

```bash
python main.py
```
