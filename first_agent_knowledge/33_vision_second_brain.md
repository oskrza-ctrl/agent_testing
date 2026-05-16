---
tags: [vision, second-brain, proyecto, roadmap, futuro]
---

# Visión del proyecto — Second Brain Agent

El Second Brain Agent es un sistema personal de captura y organización del conocimiento. El objetivo es que nunca se pierda una idea, tarea, reunión o decisión — todo lo que se dice en un audio queda organizado automáticamente.

## El problema que resuelve

Las notas de voz se acumulan sin organización. Los audios de WhatsApp con ideas quedan perdidos. Las reuniones se olvidan. Las tareas que se dicen en un audio no llegan al gestor de tareas.

## El flujo de valor

```
Hablas (MP3)
    |
    v
Transcripción automática (Whisper)
    |
    v
Clasificación inteligente (GPT-4o-mini)
    |
    v
Organización automática
    ├── Idea         → ideas.md + Obsidian
    ├── Tarea        → tasks.md + Google Tasks
    ├── Recordatorio → reminders.md + Google Calendar
    ├── Reunión      → archivo individual con secciones ricas
    ├── Proyecto     → projects.md
    └── Nota general → archivo individual
    |
    v
Sincronización a Google Drive
    |
    v
Consulta futura (fase próxima)
```

## Las fases del roadmap

| Fase | Estado | Descripción |
|------|--------|-------------|
| 0-6 | ✅ Completo | Preparación, MVP, servicios modulares |
| 7-11 | ✅ Completo | Agentes, prompts, clasificación real |
| 12 | ✅ Completo | Knowledge Base Markdown V1 |
| 13 | ✅ Completo | Google Tasks |
| 14 | ✅ Completo | Google Calendar |
| 15 | ✅ Completo | Google Drive |
| 16 | ✅ Completo | LangGraph (orquestación formal) |
| 17 | ⏸️ Pendiente | Cloud Run + Scheduler (automatización) |
| 18 | 🔮 Futuro | Agente consultable (¿qué ideas tuve esta semana?) |
| 19 | 🔮 Futuro | Interfaz conversacional (Telegram, WhatsApp) |

## El "segundo cerebro" completo

La visión final es un sistema que:
1. **Captura** automáticamente lo que dices
2. **Organiza** por tipo de contenido
3. **Recuerda** — puede consultarse ("¿qué tareas tengo del proyecto BOYA?")
4. **Sigue** — rastrea si las tareas se completaron, si los eventos pasaron
5. **Conecta** — vincula ideas relacionadas entre sí (Obsidian graph)

## Decisiones clave de diseño

- **Python** sobre JavaScript: ecosistema de IA más maduro
- **gpt-4o-mini** sobre GPT-4o: 16x más barato para la misma tarea
- **Servicios intercambiables**: no hay lock-in con OpenAI
- **Markdown primero**: compatible con Obsidian, versionable con git, legible sin herramientas
- **Google es opcional**: el sistema funciona sin credenciales de Google
- **LangGraph**: el grafo está listo para paralelización y checkpointing futuros

## Conceptos relacionados

- [[34_decisiones_tecnicas]] — las 23 decisiones documentadas
- [[25_knowledge_base]] — la base de conocimiento que genera el sistema
- [[29_langgraph_intro]] — el orquestador actual
- [[32_obsidian_wikilinks]] — cómo navegar el conocimiento generado
