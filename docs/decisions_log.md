# Decisions Log

Registro cronológico de decisiones importantes tomadas en el proyecto.

---

## 2026-05-12

### DEC-001 — Stack inicial del proyecto

**Decisión:** Usar Python como lenguaje principal del proyecto.  
**Razón:** Ecosistema maduro para IA, compatibilidad con OpenAI SDK, rapidez para prototipar.

---

### DEC-002 — Proveedor de transcripción inicial

**Decisión:** Usar OpenAI Whisper API (`whisper-1`) para transcripción de audio.  
**Razón:** Es el modelo más económico disponible (~$0.006/min), confiable y fácil de integrar. Se evaluarán alternativas (Deepgram, AssemblyAI) si el costo escala.  
**Revisión futura:** Migrar a Whisper local en Fase 1.5 para eliminar costo por token.

---

### DEC-003 — Modelo de análisis de texto

**Decisión:** Usar `gpt-4o-mini` para análisis del transcript y generación de Markdown.  
**Razón:** Relación costo/calidad superior a `gpt-4o` para tareas de clasificación y resumen de texto. Mucho más económico (~$0.15 vs $2.50 por millón de tokens de entrada).

---

### DEC-004 — Sin cloud ni LangGraph en V1

**Decisión:** Validar el pipeline completamente local antes de agregar complejidad.  
**Razón:** Reducir variables de fallo, iterar rápido y entender el flujo antes de distribuirlo.  
**Alcance:** Sin Google Drive, sin Cloud Run, sin LangGraph hasta que el flujo local sea estable.

---

### DEC-005 — Salida en Markdown plano

**Decisión:** Usar archivos Markdown como formato de salida principal, sin base de datos.  
**Razón:** Legible por humanos, compatible con Obsidian, compatible con Google Drive y fácil de versionar con git.

---

## 2026-05-14

### DEC-006 — Arquitectura de servicios modulares

**Decisión:** Diseñar el código con interfaces de servicio intercambiables desde el inicio.  
**Razón:** Evitar dependencia permanente de OpenAI. El sistema debe poder cambiar de proveedor de transcripción o análisis sin reescribir el pipeline.  
**Servicios definidos:** `TranscriptionService`, `TextAnalysisService`, `FileService`, `TaskService`, `CalendarService`.

---

### DEC-007 — Regla de calendario vs. tareas

**Decisión:** Crear eventos en Google Calendar solo cuando exista fecha **y** hora explícitas. Con fecha pero sin hora → Google Tasks. Ambiguo → Markdown como "requiere revisión".  
**Razón:** Evitar creación accidental de eventos en calendario que contaminen la agenda.

---

### DEC-008 — Ideas en archivo acumulativo, no archivos separados

**Decisión:** Las ideas se agregan a `ideas.md` en lugar de crear un archivo por cada idea.  
**Razón:** Evitar caos documental. Un archivo acumulativo es más fácil de revisar y mantener.

---

### DEC-009 — Documentación viva en el repositorio

**Decisión:** Mantener `docs/` como fuente de verdad del proyecto dentro del repo.  
**Razón:** La documentación debe evolucionar junto con el código y ser revisable antes de implementar cambios de alcance.  
**Archivos base:**
- `second_brain_agent_functional_spec.md` — alcance funcional
- `technical_spec.md` — arquitectura técnica
- `roadmap.md` — fases de desarrollo
- `decisions_log.md` — este archivo

---

## Plantilla para nuevas decisiones

```markdown
### DEC-XXX — Título de la decisión

**Decisión:** Qué se decidió hacer o no hacer.  
**Razón:** Por qué se tomó esta decisión.  
**Revisión futura:** Cuándo o bajo qué condición se debería reconsiderar (opcional).
```
