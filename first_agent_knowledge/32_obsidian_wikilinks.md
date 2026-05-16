---
tags: [obsidian, wikilinks, knowledge-management, notas, grafo]
---

# Obsidian y los [[wikilinks]]

Obsidian es una aplicación de notas que lee archivos Markdown de una carpeta local. Su superpoder es el **grafo de conocimiento**: las notas se conectan entre sí con `[[wikilinks]]` y se puede visualizar cómo se relacionan.

## Qué es un wikilink

```markdown
Ver también [[25_knowledge_base]] para entender la estructura de archivos.
```

Obsidian convierte `[[25_knowledge_base]]` en un enlace clickeable que abre la nota `25_knowledge_base.md`. Si la nota no existe, aparece en gris — una invitación a crearla.

## Estructura de una nota Obsidian

```markdown
---
tags: [python, fundamentos]
---

# Título de la nota

Contenido de la nota con conceptos y ejemplos.

## Conceptos relacionados

- [[nota_relacionada_1]] — descripción breve
- [[nota_relacionada_2]] — descripción breve
```

### Frontmatter YAML

El bloque `---` al inicio es frontmatter YAML. Obsidian lo lee como metadatos:
- `tags` → aparecen en la sidebar de tags, permiten filtrar notas
- También se pueden agregar: `aliases`, `date`, `author`

### Backlinks

Si la nota A enlaza a la nota B, la nota B muestra automáticamente "enlazada desde A" en el panel de backlinks. No hay que mantener los links manualmente en ambas notas.

## El grafo de conocimiento

En Obsidian: `Ctrl+G` abre el Graph View — una visualización de todas las notas como puntos y sus conexiones como líneas. Las notas más conectadas aparecen más grandes.

Una nota bien conectada tiene:
- Al menos 2-3 links salientes (`[[...]]`)
- Al menos 2-3 backlinks entrantes desde otras notas

## Primera_agent_knowledge como bóveda Obsidian

La carpeta `first_agent_knowledge/` está diseñada para abrirse directamente en Obsidian:

1. Abrir Obsidian
2. "Open folder as vault" → seleccionar `first_agent_knowledge/`
3. Los `[[wikilinks]]` se resuelven automáticamente
4. El Graph View muestra cómo se conectan los conceptos

## La Knowledge_Base como segunda bóveda

La carpeta `Knowledge_Base/` también puede abrirse en Obsidian. Cada audio procesado genera nuevas notas que el sistema puede conectar automáticamente en el futuro.

La visión futura es que el sistema genere `[[wikilinks]]` en las notas de la KB para conectar ideas relacionadas, reuniones sobre el mismo proyecto, etc.

## Conceptos relacionados

- [[25_knowledge_base]] — estructura de archivos de la KB
- [[33_vision_second_brain]] — rol de Obsidian en la visión del proyecto
- [[00_indice]] — el índice maestro de esta bóveda
