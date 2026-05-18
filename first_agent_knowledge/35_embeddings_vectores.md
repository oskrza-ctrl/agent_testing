---
tags: [embeddings, vectores, openai, semantica, rag]
---

# Embeddings y vectores

Un embedding es una representación matemática del significado de un texto. OpenAI lo convierte en una lista de números (vector) que captura el contexto semántico.

## El problema que resuelven

Búsqueda tradicional (por palabras):
- Query: "automatización"
- Resultado: solo encuentra textos que contengan esa palabra exacta

Búsqueda semántica (por significado):
- Query: "automatización"
- Resultado: encuentra "scripts para no hacer tareas repetitivas", "flujos automáticos", "pipelines"

## Cómo funciona un embedding

```
"usar IA para organizar notas"
            ↓
OpenAI text-embedding-3-small
            ↓
[0.023, -0.451, 0.817, ..., 0.102]  ← 1536 números
```

Cada número representa una dimensión del significado. Textos con significado similar producen vectores similares (cercanos en el espacio matemático).

## Modelos de embedding en el proyecto

```python
# services/rag/chromadb_rag_service.py
model = "text-embedding-3-small"
```

| Modelo | Dimensiones | Costo | Uso |
|--|--|--|--|
| text-embedding-3-small | 1536 | ~$0.02/M tokens | Este proyecto |
| text-embedding-3-large | 3072 | ~$0.13/M tokens | Mayor precisión |

## Distancia entre vectores

Para saber si dos textos son similares se mide la distancia coseno entre sus vectores. Valores cercanos a 0 = muy similares, cercanos a 2 = muy distintos.

```python
DISTANCE_THRESHOLD = 1.0  # en chromadb_rag_service.py
# Resultados con distancia > 1.0 se descartan por irrelevantes
```

## Conceptos relacionados

- [[36_chromadb_rag]] — cómo se almacenan y consultan los vectores
- [[13_openai_gpt4o_mini]] — el modelo que usa los resultados de búsqueda para responder
