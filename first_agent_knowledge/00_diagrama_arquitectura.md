---
tags: [diagrama, arquitectura, agentes, langgraph, overview]
---

# Diagrama de arquitectura — Second Brain Agent

---

## Vista 1 — Flujo completo del pipeline

```mermaid
flowchart TD
    MP3[/"🎵 audio.mp3\ninput/"/]

    subgraph ORCH["OrchestratorAgent"]
        direction TB

        subgraph GRAPH["LangGraph StateGraph"]
            direction TB

            T["🎙️ TranscriptionAgent\n─────────────────\nWhisper-1 API\n→ produce: transcript"]
            AN["🧠 AnalysisAgent\n─────────────────\nGPT-4o-mini\n+ prompts/analysis_agent.md\n→ produce: AnalysisResult"]
            MK["📄 MarkdownAgent\n─────────────────\nbackup en output/\n→ produce: audio.md"]
            KB["🗂️ KnowledgeBaseAgent\n─────────────────\nACCUMULATIVE: ideas, tasks,\nreminders, projects\nINDIVIDUAL: Meetings, Notes\n+ secondary routing\n→ produce: Knowledge_Base/**"]
            DS["☁️ DriveSync\n─ opcional ─\nupload KB files\n→ Drive/knowledge_base/"]
            TA["✅ TasksAgent\n─ opcional ─\nreglas + dedup SHA256\n→ Google Tasks"]
            CA["📅 CalendarAgent\n─ opcional ─\nreglas + dedup SHA256\n→ Google Calendar"]
            AR["📦 ArchiveAgent\n─────────────────\nshutil.move\n→ processed/audio.mp3"]
            DP["☁️ DriveProcessed\n─ opcional ─\nmove in Drive\n→ Drive/processed/"]

            T --> AN
            AN --> MK
            MK --> KB
            KB --> DS
            DS --> TA
            TA --> CA
            CA --> AR
            AR --> DP
        end

        STATE(["PipelineState\n─────────────\nmp3_path\ntranscript\nresult\nerror"])
    end

    MP3 --> T
    GRAPH -. "fluye por todos los nodos" .-> STATE
```

---

## Vista 2 — Agentes, APIs y outputs

```mermaid
flowchart LR
    subgraph AGENTS["Agentes"]
        T["TranscriptionAgent"]
        AN["AnalysisAgent"]
        MK["MarkdownAgent"]
        KB["KnowledgeBaseAgent"]
        TA["TasksAgent"]
        CA["CalendarAgent"]
        AR["ArchiveAgent"]
        DS["DriveAgent"]
    end

    subgraph APIS["APIs externas"]
        OAW["OpenAI\nWhisper-1"]
        OAG["OpenAI\nGPT-4o-mini"]
        GT["Google\nTasks API"]
        GC["Google\nCalendar API"]
        GD["Google\nDrive API"]
    end

    subgraph OUTPUTS["Outputs"]
        O1["output/\ntranscript.txt\naudio.md"]
        O2["Knowledge_Base/\nIdeas/ideas.md\nTasks/tasks.md\nMeetings/*.md\nReminders/reminders.md\nProjects/projects.md\nGeneral_Notes/*.md"]
        O3["Google Tasks\nlista 'Second Brain Agent'"]
        O4["Google Calendar\neventos con fecha+hora"]
        O5["processed/\naudio.mp3"]
        O6["Drive/\nknowledge_base/**\nprocessed/audio.mp3"]
    end

    T -->|transcript| OAW
    AN -->|análisis| OAG
    TA -->|crear task| GT
    CA -->|crear event| GC
    DS -->|upload/move| GD

    T --> O1
    MK --> O1
    KB --> O2
    TA --> O3
    CA --> O4
    AR --> O5
    DS --> O6
```

---

## Vista 3 — Reglas de enrutado de contenido

```mermaid
flowchart TD
    AR[/"AnalysisResult\ncategory + tasks\n+ reminders + ideas"/]

    AR --> CAT{¿Categoría?}

    CAT -->|Idea| IDEA["ideas.md\n(acumulativo)"]
    CAT -->|Tarea| TASK["tasks.md\n(acumulativo)"]
    CAT -->|Recordatorio| REM["reminders.md\n(acumulativo)"]
    CAT -->|Proyecto| PROJ["projects.md\n(acumulativo)"]
    CAT -->|Reunión| MTG["Meetings/\nYYYY-MM-DD_titulo.md\n(individual, secciones ricas)"]
    CAT -->|Nota general| NOTE["General_Notes/\nYYYY-MM-DD_titulo.md\n(individual)"]

    MTG --> SEC{Elementos secundarios}
    NOTE --> SEC

    SEC -->|tasks[]| TASK
    SEC -->|reminders[]| REM
    SEC -->|ideas[]| IDEA

    TASK --> TRULE{Regla de tarea}
    REM --> RRULE{Regla de recordatorio}

    TRULE -->|sin fecha| GTASK7["Google Task\ndue: hoy +7 días"]
    TRULE -->|con fecha| GTASKD["Google Task\ndue: fecha indicada"]
    TRULE -->|ambiguo| MDONLY1["Solo Markdown"]

    RRULE -->|candidato: Google Tasks| GTASKR["Google Task\ncon due date"]
    RRULE -->|candidato: Google Calendar| GCAL["Google Calendar\nevento 1h"]
    RRULE -->|ambiguo / sin marcador| MDONLY2["Solo Markdown"]
```

---

## Leyenda

| Símbolo | Significado |
|---------|-------------|
| `─ opcional ─` | Solo se ejecuta si las credenciales de Google están configuradas |
| `→ PipelineState` | El estado fluye entre todos los nodos de LangGraph |
| `SHA256 dedup` | Antes de crear, se verifica si ya existe en `created_tasks.json` / `created_events.json` |
| `ACCUMULATIVE` | Varias entradas en un solo archivo (ideas.md, tasks.md) |
| `INDIVIDUAL` | Un archivo por entrada (Meetings/, General_Notes/) |

## Conceptos relacionados

- [[31_langgraph_pipeline]] — los 9 nodos en detalle
- [[25_knowledge_base]] — ACCUMULATIVE vs INDIVIDUAL
- [[27_reglas_calendario_tareas]] — la tabla de reglas de enrutado
- [[21_arquitectura_agentes]] — responsabilidad de cada agente
