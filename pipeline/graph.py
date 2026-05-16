from langgraph.graph import StateGraph, END

from pipeline.state import PipelineState
from pipeline.nodes import (
    make_transcription_node,
    make_analysis_node,
    make_markdown_node,
    make_kb_node,
    make_drive_sync_node,
    make_tasks_node,
    make_calendar_node,
    make_archive_node,
    make_drive_processed_node,
)


def build_graph(agents: dict, dirs: dict):
    """
    Build and compile the LangGraph pipeline.

    agents dict keys:
        transcription, analysis, markdown, kb, tasks, calendar, archive,
        drive (optional), drive_sync_fn (optional)
    dirs dict keys:
        output, kb
    """
    graph = StateGraph(PipelineState)

    graph.add_node("transcription",   make_transcription_node(agents, dirs))
    graph.add_node("analysis",        make_analysis_node(agents))
    graph.add_node("markdown",        make_markdown_node(agents, dirs))
    graph.add_node("knowledge_base",  make_kb_node(agents))
    graph.add_node("drive_sync",      make_drive_sync_node(agents))
    graph.add_node("tasks",           make_tasks_node(agents))
    graph.add_node("calendar",        make_calendar_node(agents))
    graph.add_node("archive",         make_archive_node(agents))
    graph.add_node("drive_processed", make_drive_processed_node(agents))

    graph.set_entry_point("transcription")

    sequence = [
        ("transcription",   "analysis"),
        ("analysis",        "markdown"),
        ("markdown",        "knowledge_base"),
        ("knowledge_base",  "drive_sync"),
        ("drive_sync",      "tasks"),
        ("tasks",           "calendar"),
        ("calendar",        "archive"),
        ("archive",         "drive_processed"),
        ("drive_processed", END),
    ]
    for src, dst in sequence:
        graph.add_edge(src, dst)

    return graph.compile()
