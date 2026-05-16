---
tags: [knowledge-base, markdown, estructura, archivos, obsidian]
---

# Knowledge Base — estructura y enrutado

La Knowledge Base es el archivo de salida principal del sistema. Es una colección de archivos Markdown organizados por tipo de contenido, compatible con Obsidian.

## Estructura de carpetas

```
Knowledge_Base/
├── Ideas/
│   └── ideas.md              (acumulativo — todas las ideas en un solo archivo)
├── Tasks/
│   ├── tasks.md              (acumulativo)
│   └── created_tasks.json    (registro de tareas creadas en Google Tasks)
├── Meetings/
│   └── 2026-05-15_reunion_boya.md   (individual por reunión)
├── Reminders/
│   ├── reminders.md          (acumulativo)
│   └── created_events.json   (registro de eventos creados en Google Calendar)
├── Projects/
│   └── projects.md           (acumulativo)
└── General_Notes/
    └── 2026-05-15_nota_titulo.md    (individual)
```

## Dos tipos de archivos: ACCUMULATIVE vs INDIVIDUAL

```python
# Categorías acumulativas — todo en un archivo
ACCUMULATIVE = {
    "Idea":         ("Ideas",     "ideas.md",     "# Ideas\n\n"),
    "Tarea":        ("Tasks",     "tasks.md",      "# Tareas\n\n"),
    "Recordatorio": ("Reminders", "reminders.md",  "# Recordatorios\n\n"),
    "Proyecto":     ("Projects",  "projects.md",   "# Proyectos\n\n"),
}

# Categorías que generan un archivo por entrada
INDIVIDUAL = {
    "Reunion":      "Meetings",
    "Nota general": "General_Notes",
}
```

**Acumulativo:** cada nueva entrada se append al final del archivo. Es como un diario.  
**Individual:** cada entrada tiene su propio archivo con nombre `YYYY-MM-DD_titulo.md`.

## Enrutado secundario

Las categorías individuales (Reunión, Nota general) también derivan sus elementos secundarios:

```python
SECONDARY_ROUTES = {
    "tasks":     ("Tasks",     "tasks.md",     "# Tareas\n\n"),
    "reminders": ("Reminders", "reminders.md", "# Recordatorios\n\n"),
    "ideas":     ("Ideas",     "ideas.md",     "# Ideas\n\n"),
}
```

Si una Reunión tiene tareas e ideas, esos elementos también aparecen en `tasks.md` e `ideas.md`. Ningún elemento accionable se pierde en el archivo de la reunión.

## Sincronización con Google Drive

Después de cada procesamiento, los archivos KB modificados se suben a Drive:

```
Drive/second_brain/knowledge_base/Ideas/ideas.md
Drive/second_brain/knowledge_base/Tasks/tasks.md
...
```

Se sube archivo por archivo (no al final del batch) para que si el sistema falla a mitad, los archivos ya procesados estén seguros en Drive.

## Compatibilidad con Obsidian

Los archivos `.md` son leíbles directamente en Obsidian. Se puede apuntar Obsidian a la carpeta `Knowledge_Base/` y navegar el grafo de notas con backlinks y tags.

## Conceptos relacionados

- [[24_categorias_contenido]] — qué categoría va a qué carpeta
- [[26_deduplicacion]] — cómo evitar duplicados en Google Tasks y Calendar
- [[32_obsidian_wikilinks]] — cómo navegar la KB en Obsidian
- [[19_google_drive_api]] — sincronización a Drive
