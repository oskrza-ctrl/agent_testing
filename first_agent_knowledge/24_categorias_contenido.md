---
tags: [categorias, clasificacion, contenido, analisis]
---

# Las 6 categorías de contenido

El sistema clasifica cada audio en una de 6 categorías. La categoría determina cómo y dónde se guarda el contenido.

## Las 6 categorías

### Idea
**Cuándo:** El contenido principal es una idea, concepto, reflexión o propuesta.  
**Salida:** Entrada en `Knowledge_Base/Ideas/ideas.md` (archivo acumulativo).  
**Ejemplo:** "Quiero automatizar el procesamiento de facturas con IA"

### Tarea
**Cuándo:** El audio describe principalmente algo que hay que hacer.  
**Salida:** Entrada en `tasks.md` + Google Task.  
**Ejemplo:** "Tengo que llamar al banco para preguntar por los cargos del mes pasado"

### Recordatorio
**Cuándo:** Hay una referencia temporal explícita (fecha, hora, día de la semana).  
**Salida:** Entrada en `reminders.md` + Google Task (solo fecha) o Google Calendar (fecha + hora).  
**Ejemplo:** "El jueves a las 3pm tengo cita con el dentista"

### Reunión
**Cuándo:** El audio describe o resume una reunión con otras personas.  
**Salida:** Archivo individual en `Knowledge_Base/Meetings/YYYY-MM-DD_titulo.md` con secciones ricas (Participantes, Decisiones, Acciones, etc.).  
**Ejemplo:** "En la reunión con el equipo de BOYA decidimos..."

### Proyecto
**Cuándo:** El contenido describe un proyecto, iniciativa o área de trabajo.  
**Salida:** Entrada en `Knowledge_Base/Projects/projects.md` (acumulativo).  
**Ejemplo:** "Quiero crear un sistema de segundo cerebro con IA"

### Nota general
**Cuándo:** El contenido no encaja claramente en ninguna categoría anterior.  
**Salida:** Archivo individual en `Knowledge_Base/General_Notes/YYYY-MM-DD_titulo.md`.  
**Ejemplo:** Una reflexión personal sin tareas concretas ni fecha

## Regla de categoría vs. elementos secundarios

La categoría principal determina la carpeta de destino, pero **los elementos secundarios se enrutan a sus propios archivos**.

Si un audio es clasificado como "Reunión" pero durante la reunión se mencionaron tareas e ideas, esas tareas e ideas también se agregan a `tasks.md` e `ideas.md` respectivamente.

```
Audio: "Reunión con el equipo BOYA"
↓
category = "Reunión"   → Meetings/2026-05-15_reunion_boya.md
tasks[]   → Tasks/tasks.md (también)
ideas[]   → Ideas/ideas.md (también)
reminders[] → Reminders/reminders.md (también)
```

## Regla de fechas — NUNCA inventar

El modelo tiene la instrucción explícita de **nunca** convertir referencias relativas en fechas absolutas. "Mañana" se preserva como "mañana" y se marca con `[candidato: Google Tasks]` o `[candidato: Google Calendar]`.

En pruebas tempranas, GPT generaba fechas como "2023-10-12" para "mañana", contaminando el calendario con eventos en el pasado. La regla lo corrige.

## Conceptos relacionados

- [[23_analysis_result]] — el campo `category` del resultado
- [[25_knowledge_base]] — ACCUMULATIVE vs INDIVIDUAL
- [[27_reglas_calendario_tareas]] — lógica de derivación de Recordatorio a Task/Event
