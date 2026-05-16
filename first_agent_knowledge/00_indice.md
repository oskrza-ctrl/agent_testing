---
tags: [indice, second-brain, navegacion]
---

# Indice — First Agent Knowledge

Esta bóveda documenta todo lo necesario para entender y replicar el proyecto **Second Brain Agent**, desde conceptos básicos de Python hasta LangGraph.

---

## Grupo A — Python fundamentals

- [[01_python_variables_tipos]] — Variables, tipos básicos, strings, listas, dicts
- [[02_python_funciones]] — Funciones, parámetros, retorno, default args
- [[03_python_clases_oop]] — Clases, `__init__`, herencia, métodos
- [[04_python_modulos_imports]] — Imports, paquetes, `__init__.py`
- [[05_python_pathlib]] — Manejo de archivos y rutas con `Path`
- [[06_python_errores]] — `try/except`, excepciones, `raise`
- [[07_python_dataclasses_typeddict]] — `@dataclass`, `TypedDict`, type hints
- [[08_python_dotenv]] — Variables de entorno, `.env`, `python-dotenv`

---

## Grupo B — APIs y autenticación

- [[09_apis_rest]] — Qué es una API REST, HTTP, JSON
- [[10_autenticacion_apis]] — API Keys vs OAuth2
- [[11_openai_overview]] — OpenAI API, modelos, pricing
- [[12_openai_whisper]] — Transcripción de audio con Whisper-1
- [[13_openai_gpt4o_mini]] — Análisis de texto, prompts, temperature
- [[14_openai_json_mode]] — `response_format`, parsing de JSON
- [[15_google_apis_overview]] — Google Cloud Console, credenciales, scopes
- [[16_google_oauth2]] — Flujo OAuth2, tokens, refresh automático

---

## Grupo C — Google APIs específicas

- [[17_google_tasks_api]] — Crear listas y tareas, due dates
- [[18_google_calendar_api]] — Crear eventos, timezone, scopes
- [[19_google_drive_api]] — Listar, descargar, subir, mover archivos

---

## Grupo D — Arquitectura del proyecto

- [[20_arquitectura_servicios]] — Patrón de servicios intercambiables
- [[21_arquitectura_agentes]] — Agentes vs servicios, responsabilidades
- [[22_prompts_markdown]] — Sistema de prompts en archivos `.md`
- [[23_analysis_result]] — Dataclass AnalysisResult, 15 campos
- [[24_categorias_contenido]] — Las 6 categorías del sistema
- [[25_knowledge_base]] — Estructura KB, enrutado de archivos

---

## Grupo E — Funciones especiales del sistema

- [[26_deduplicacion]] — Hash SHA256, JSON de tracking
- [[27_reglas_calendario_tareas]] — Cuándo crear Task vs Event vs solo Markdown
- [[28_manejo_errores_pipeline]] — Early return, error propagation

---

## Grupo F — LangGraph

- [[29_langgraph_intro]] — Qué es LangGraph y por qué usarlo
- [[30_langgraph_stategraph]] — `StateGraph`, nodos, edges, TypedDict state
- [[31_langgraph_pipeline]] — Los 9 nodos del proyecto

---

## Grupo G — Visión y contexto

- [[32_obsidian_wikilinks]] — Cómo usar Obsidian, [[wikilinks]], backlinks
- [[33_vision_second_brain]] — Visión completa del proyecto
- [[34_decisiones_tecnicas]] — Las 23 decisiones clave del proyecto

---

## Punto de entrada recomendado

Si eres nuevo en el proyecto, empieza aquí:

1. [[33_vision_second_brain]] — entiende qué resuelve el sistema
2. [[01_python_variables_tipos]] — fundamentos de Python
3. [[09_apis_rest]] — cómo funciona una API
4. [[11_openai_overview]] — OpenAI en el proyecto
5. [[20_arquitectura_servicios]] — cómo está organizado el código
6. [[29_langgraph_intro]] — el orquestador final
