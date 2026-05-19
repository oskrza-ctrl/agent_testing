"""
api.py — Entrypoint HTTP del Second Brain Agent (FastAPI).

Uso:
    python api.py

Endpoints:
    GET   /health                                  — estado del servicio
    POST  /chat                                    — mensaje de texto → respuesta del agente
    GET   /kb/{category}                           — contenido de una categoría de la Knowledge Base
    PATCH /kb/ideas/{entry_title}                  — editar resumen de una idea
    PATCH /kb/projects/{project_name}/progress     — actualizar progreso de un proyecto
    POST  /kb/projects/{project_name}/comments     — agregar comentario a un proyecto
    GET   /kb/meetings/{filename}/download         — descargar archivo MD de una reunión
"""
import os
import re
from datetime import date
from pathlib import Path

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from core.agent_factory import build_message_handler

load_dotenv()

app = FastAPI(title="Second Brain Agent API")


@app.on_event("startup")
def startup():
    from core.agent_factory import _write_google_credentials_from_env
    _write_google_credentials_from_env()
    _download_kb_from_drive()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

KB_CATEGORIES = {"ideas", "tasks", "meetings", "reminders", "projects", "notes"}
KB_FOLDER_MAP = {
    "ideas":     "Ideas/ideas.md",
    "tasks":     "Tasks/tasks.md",
    "reminders": "Reminders/reminders.md",
    "projects":  "Projects/projects.md",
    "meetings":  "Meetings",
    "notes":     "General_Notes",
}

_handler = None


def _download_kb_from_drive() -> None:
    """Download Knowledge Base from Google Drive before serving requests."""
    kb_folder_id  = os.getenv("GOOGLE_DRIVE_KB_FOLDER_ID", "")
    drive_token   = Path(os.getenv("GOOGLE_DRIVE_TOKEN_FILE", "credentials/token_drive.json"))
    creds_file    = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials/credentials.json"))

    if not kb_folder_id or not creds_file.exists():
        print("[api] Google Drive no configurado — KB local vacía.")
        return
    try:
        from services.drive.google_drive_service import GoogleDriveService
        from agents.drive_agent import DriveAgent
        svc   = GoogleDriveService(creds_file, drive_token)
        agent = DriveAgent(
            drive_svc           = svc,
            inbox_folder_id     = os.getenv("GOOGLE_DRIVE_INBOX_FOLDER_ID", ""),
            processed_folder_id = os.getenv("GOOGLE_DRIVE_PROCESSED_FOLDER_ID", ""),
            kb_folder_id        = kb_folder_id,
            local_input_dir     = Path("input"),
            local_kb_dir        = Path("Knowledge_Base"),
        )
        agent.download_kb()
    except Exception as e:
        print(f"[api] No se pudo descargar KB de Drive: {e}")


def _upload_file_to_drive(local_file: Path) -> None:
    """Upload a single KB file back to Google Drive after a write operation."""
    kb_folder_id = os.getenv("GOOGLE_DRIVE_KB_FOLDER_ID", "")
    drive_token  = Path(os.getenv("GOOGLE_DRIVE_TOKEN_FILE", "credentials/token_drive.json"))
    creds_file   = Path(os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials/credentials.json"))

    if not kb_folder_id or not creds_file.exists():
        return
    try:
        from services.drive.google_drive_service import GoogleDriveService
        from agents.drive_agent import DriveAgent
        svc   = GoogleDriveService(creds_file, drive_token)
        agent = DriveAgent(
            drive_svc           = svc,
            inbox_folder_id     = os.getenv("GOOGLE_DRIVE_INBOX_FOLDER_ID", ""),
            processed_folder_id = os.getenv("GOOGLE_DRIVE_PROCESSED_FOLDER_ID", ""),
            kb_folder_id        = kb_folder_id,
            local_input_dir     = Path("input"),
            local_kb_dir        = Path("Knowledge_Base"),
        )
        agent.upload_kb_file(local_file)
    except Exception as e:
        print(f"[api] No se pudo subir {local_file.name} a Drive: {e}")


def get_handler():
    global _handler
    if _handler is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY no configurada.")
        _handler = build_message_handler(api_key=api_key)
    return _handler


# ── Schemas ───────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class EditIdeaRequest(BaseModel):
    summary: str

class UpdateProgressRequest(BaseModel):
    progress: int

class AddCommentRequest(BaseModel):
    comment: str


# ── Endpoints ─────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/kb/sync")
def kb_sync():
    """Force a full KB download from Google Drive."""
    _download_kb_from_drive()
    return {"ok": True, "message": "KB sincronizada desde Drive"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")
    response = get_handler().process_message(req.message)
    return ChatResponse(response=response)


@app.get("/kb/{category}")
def kb(category: str):
    """Return the content of a KB category as plain text."""
    if category not in KB_CATEGORIES:
        raise HTTPException(
            status_code=404,
            detail=f"Categoría no válida. Opciones: {sorted(KB_CATEGORIES)}",
        )
    kb_dir  = Path("Knowledge_Base")
    target  = kb_dir / KB_FOLDER_MAP[category]

    # Accumulative files (single .md)
    if target.suffix == ".md":
        if not target.exists():
            return {"category": category, "content": ""}
        return {"category": category, "content": target.read_text(encoding="utf-8")}

    # Individual files (folder with multiple .md)
    if not target.exists():
        return {"category": category, "files": []}
    files = sorted(target.glob("*.md"), reverse=True)
    return {
        "category": category,
        "files": [
            {"name": f.name, "content": f.read_text(encoding="utf-8")}
            for f in files
        ],
    }


# ── KB write endpoints ────────────────────────────────────────────

@app.patch("/kb/ideas/{entry_title}")
def edit_idea(entry_title: str, req: EditIdeaRequest):
    """Replace the Resumen field of an idea entry identified by its title."""
    ideas_file = Path("Knowledge_Base/Ideas/ideas.md")
    if not ideas_file.exists():
        raise HTTPException(status_code=404, detail="Archivo de ideas no encontrado.")

    content = ideas_file.read_text(encoding="utf-8")

    # Find the entry block starting with ## <title>
    pattern = re.compile(
        rf"(## {re.escape(entry_title)}.*?)"   # header + content up to Resumen
        rf"(\*\*Resumen:\*\*[^\n]*)",          # Resumen line to replace
        re.DOTALL,
    )
    if not pattern.search(content):
        raise HTTPException(status_code=404, detail=f"Idea '{entry_title}' no encontrada.")

    updated = pattern.sub(
        lambda m: m.group(1) + f"**Resumen:** {req.summary}",
        content,
        count=1,
    )
    ideas_file.write_text(updated, encoding="utf-8")
    _upload_file_to_drive(ideas_file)
    return {"ok": True}


@app.patch("/kb/projects/{project_name}/progress")
def update_project_progress(project_name: str, req: UpdateProgressRequest):
    """Update or add a Progreso field in a project's MD file."""
    if not (0 <= req.progress <= 100):
        raise HTTPException(status_code=400, detail="El progreso debe estar entre 0 y 100.")

    projects_file = Path("Knowledge_Base/Projects/projects.md")
    if not projects_file.exists():
        raise HTTPException(status_code=404, detail="Archivo de proyectos no encontrado.")

    content = projects_file.read_text(encoding="utf-8")

    progress_line = f"**Progreso:** {req.progress}%"
    progress_pattern = re.compile(r"\*\*Progreso:\*\*[^\n]*")

    # Find the project block
    project_pattern = re.compile(
        rf"(## {re.escape(project_name)}.*?)(\n## |\Z)",
        re.DOTALL,
    )
    match = project_pattern.search(content)
    if not match:
        raise HTTPException(status_code=404, detail=f"Proyecto '{project_name}' no encontrado.")

    block = match.group(1)
    if progress_pattern.search(block):
        updated_block = progress_pattern.sub(progress_line, block, count=1)
    else:
        updated_block = block.rstrip() + f"\n{progress_line}\n"

    updated = content[:match.start(1)] + updated_block + content[match.start(2):]
    projects_file.write_text(updated, encoding="utf-8")
    _upload_file_to_drive(projects_file)
    return {"ok": True}


@app.post("/kb/projects/{project_name}/comments")
def add_project_comment(project_name: str, req: AddCommentRequest):
    """Append a dated comment to a project entry."""
    projects_file = Path("Knowledge_Base/Projects/projects.md")
    if not projects_file.exists():
        raise HTTPException(status_code=404, detail="Archivo de proyectos no encontrado.")

    content = projects_file.read_text(encoding="utf-8")

    project_pattern = re.compile(
        rf"(## {re.escape(project_name)}.*?)(\n## |\Z)",
        re.DOTALL,
    )
    match = project_pattern.search(content)
    if not match:
        raise HTTPException(status_code=404, detail=f"Proyecto '{project_name}' no encontrado.")

    today = date.today().isoformat()
    new_comment = f"- {today}: {req.comment}"
    block = match.group(1)

    if "## Comentarios" in block:
        updated_block = block.rstrip() + f"\n{new_comment}\n"
    else:
        updated_block = block.rstrip() + f"\n\n## Comentarios\n{new_comment}\n"

    updated = content[:match.start(1)] + updated_block + content[match.start(2):]
    projects_file.write_text(updated, encoding="utf-8")
    _upload_file_to_drive(projects_file)
    return {"ok": True}


@app.get("/kb/meetings/{filename}/download")
def download_meeting(filename: str):
    """Download a meeting MD file as an attachment."""
    meetings_dir = Path("Knowledge_Base/Meetings")
    file_path = meetings_dir / filename

    if not file_path.exists() or file_path.suffix != ".md":
        raise HTTPException(status_code=404, detail=f"Reunión '{filename}' no encontrada.")

    return FileResponse(
        path=str(file_path),
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


# ── Main ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)
