from dataclasses import dataclass
from typing import List


@dataclass
class AnalysisResult:
    category: str         # Categoría principal: Idea, Reunión, Tarea, Recordatorio, Proyecto, Nota general
    title: str            # Título sugerido para el archivo
    summary: str          # Resumen breve del contenido
    ideas: List[str]      # Ideas detectadas
    tasks: List[str]      # Tareas accionables (con fecha si aplica)
    reminders: List[str]  # Recordatorios (con referencia temporal original)
    related_project: str  # Proyecto relacionado o "No asignado"
    ambiguity_notes: str  # Elementos ambiguos que requieren revisión
    tags: List[str]       # Palabras clave relevantes (siempre al menos 2)
    participants: List[str]      # Personas mencionadas (principal uso: Reunión)
    decisions: List[str]         # Conclusiones o acuerdos tomados (principal uso: Reunión)
    actions_for_me: List[str]    # Acciones que debe hacer quien grabó (principal uso: Reunión)
    actions_for_others: List[str]# Acciones asignadas a otras personas (principal uso: Reunión)
    risks_blockers: List[str]    # Riesgos o bloqueos mencionados (principal uso: Reunión)
    next_steps: List[str]        # Próximos pasos detectados (principal uso: Reunión)
