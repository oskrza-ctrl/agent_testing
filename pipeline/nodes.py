"""
Node factory functions for the LangGraph pipeline.

Each factory receives the pre-built agents and dirs, and returns a node function.
Node functions receive PipelineState and return a partial state update (dict).
If state["error"] is set, they skip execution and return {}.
"""
from pathlib import Path
from pipeline.state import PipelineState
from services.file_service import save_text


# ── Transcription ─────────────────────────────────────

def make_transcription_node(agents: dict, dirs: dict):
    agent      = agents["transcription"]
    output_dir = dirs["output"]

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        try:
            transcript = agent.run(state["mp3_path"])
            save_text(output_dir / f"{state['mp3_stem']}_transcript.txt", transcript)
            return {"transcript": transcript}
        except Exception as e:
            return {"error": f"[transcription] {e}"}

    return node


# ── Analysis ──────────────────────────────────────────

def make_analysis_node(agents: dict):
    agent = agents["analysis"]

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        try:
            result = agent.run(state["transcript"])
            print(f"[OrchestratorAgent] Category: {result.category} | Title: {result.title}")
            return {"result": result}
        except Exception as e:
            return {"error": f"[analysis] {e}"}

    return node


# ── Markdown ──────────────────────────────────────────

def make_markdown_node(agents: dict, dirs: dict):
    agent      = agents["markdown"]
    output_dir = dirs["output"]

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        try:
            agent.run(output_dir, state["mp3_stem"], state["transcript"], state["result"])
            return {}
        except Exception as e:
            return {"error": f"[markdown] {e}"}

    return node


# ── Knowledge Base ────────────────────────────────────

def make_kb_node(agents: dict):
    agent = agents["kb"]

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        try:
            agent.run(state["result"], state["mp3_name"])
            return {}
        except Exception as e:
            return {"error": f"[knowledge_base] {e}"}

    return node


# ── Drive sync (optional) ─────────────────────────────

def make_drive_sync_node(agents: dict):
    orchestrator = agents.get("orchestrator_ref")

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        drive = agents.get("drive")
        if not drive:
            return {}
        try:
            # Reuse the sync logic via the reference stored in agents dict
            sync_fn = agents.get("drive_sync_fn")
            if sync_fn:
                sync_fn(state["result"])
            return {}
        except Exception as e:
            print(f"[DriveAgent] Sync warning: {e}")
            return {}

    return node


# ── Tasks (optional) ──────────────────────────────────

def make_tasks_node(agents: dict):
    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        agent = agents.get("tasks")
        if not agent:
            return {}
        try:
            agent.run(state["result"], state["mp3_name"])
            return {}
        except Exception as e:
            print(f"[TasksAgent] Warning: {e}")
            return {}

    return node


# ── Calendar (optional) ───────────────────────────────

def make_calendar_node(agents: dict):
    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        agent = agents.get("calendar")
        if not agent:
            return {}
        try:
            agent.run(state["result"], state["mp3_name"])
            return {}
        except Exception as e:
            print(f"[CalendarAgent] Warning: {e}")
            return {}

    return node


# ── Archive ───────────────────────────────────────────

def make_archive_node(agents: dict):
    agent = agents["archive"]

    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        try:
            agent.run(state["mp3_path"])
            return {}
        except Exception as e:
            return {"error": f"[archive] {e}"}

    return node


# ── Drive move to processed (optional) ───────────────

def make_drive_processed_node(agents: dict):
    def node(state: PipelineState) -> dict:
        if state.get("error"):
            return {}
        drive = agents.get("drive")
        if not drive:
            return {}
        try:
            drive.move_to_processed(state["mp3_name"])
            return {}
        except Exception as e:
            print(f"[DriveAgent] Move warning: {e}")
            return {}

    return node
