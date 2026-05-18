---
tags: [chromadb, rag, vectorstore, busqueda-semantica]
---

# ChromaDB y RAG

## Qué es RAG

RAG (Retrieval Augmented Generation) es el patrón de combinar búsqueda en una base de conocimiento con generación de texto por un LLM.

Sin RAG: GPT responde solo con su conocimiento de entrenamiento (no sabe nada de tu KB).
Con RAG: GPT recibe fragmentos relevantes de tu KB como contexto y responde basándose en ellos.

```
Pregunta del usuario
        ↓
Buscar fragmentos relevantes en ChromaDB
        ↓
Construir prompt: fragmentos + pregunta
        ↓
GPT-4o-mini genera respuesta basada en tu KB
        ↓
Respuesta personalizada y precisa
```

## Qué es ChromaDB

Base de datos de vectores local. Guarda los embeddings de tu Knowledge Base y permite buscar por similitud semántica.

- **Local**: vive en `chroma_db/` en tu máquina o servidor
- **Persistente**: sobrevive reinicios (a menos que el servidor sea efímero como Railway sin volumen)
- **Gratuito**: sin infraestructura externa, sin costo por consulta

## Flujo completo en el proyecto

### Indexación (cuando se captura algo nuevo)

```
Knowledge_Base/*.md
        ↓
Leer todos los archivos Markdown
        ↓
Dividir en fragmentos (chunks)
        ↓
OpenAI text-embedding-3-small → vectores
        ↓
ChromaDB.add() → guarda vectores + texto original
```

### Consulta (cuando el usuario pregunta)

```
"¿qué ideas tengo sobre productividad?"
        ↓
OpenAI text-embedding-3-small → vector de la pregunta
        ↓
ChromaDB.query() → top 5 fragmentos más cercanos
        ↓
QueryAgent construye prompt con esos fragmentos
        ↓
GPT-4o-mini responde
```

## Configuración en el proyecto

```python
# services/rag/chromadb_rag_service.py
DISTANCE_THRESHOLD = 1.0   # descartar resultados poco relevantes
TOP_K = 5                   # máximo 5 fragmentos por consulta
```

## Re-indexación

Cada vez que se captura algo nuevo, se re-indexa toda la KB:

```python
self.rag_service.index_kb(self.kb_dir)
```

Esto borra y reconstruye todos los vectores. Es simple y siempre fresco. Tarda menos de 2 segundos para una KB pequeña.

## Dónde vive en el proyecto

```
chroma_db/           ← base de datos de vectores (gitignored)
services/rag/
  chromadb_rag_service.py  ← indexación + consulta
  intent_classifier.py     ← clasifica intención del mensaje
  action_classifier.py     ← clasifica tipo de acción (nivel 2)
```

## Limitación en Railway (sin volumen)

En Railway, `chroma_db/` es efímero — se borra al redesplegar. La Knowledge Base en Markdown persiste, pero los vectores se pierden. Se reconstruyen automáticamente la próxima vez que se captura algo o se reinicia el agente.

## Conceptos relacionados

- [[35_embeddings_vectores]] — qué son los vectores y cómo se generan
- [[37_intent_classifier]] — cómo se decide si una consulta es QUERY o CAPTURE
- [[25_knowledge_base]] — la KB que se indexa
