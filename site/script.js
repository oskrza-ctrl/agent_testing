/* ─── Roadmap Data ──────────────────────────────────── */
const ROADMAP = [
  {
    num: 0, title: "Preparación inicial", status: "done", icon: "🏁",
    summary: "Repositorio, VS Code y Claude Code configurados.",
    details: [
      "Repositorio agent_testing en GitHub",
      "VS Code con el proyecto abierto",
      "Claude Code configurado",
      "CLAUDE.md base creado"
    ],
    evidence: "CLAUDE.md, .gitignore y README.md presentes en raíz"
  },
  {
    num: 1, title: "Estructura base", status: "done", icon: "📁",
    summary: "Carpetas iniciales y archivos base del proyecto.",
    details: [
      "input/, output/, services/, prompts/",
      "main.py como punto de entrada",
      "requirements.txt con dependencias",
      ".env.example y .gitignore"
    ],
    evidence: "Estructura de carpetas verificada en el repositorio"
  },
  {
    num: 2, title: "Configuración de API", status: "done", icon: "🔑",
    summary: "Conexión segura con OpenAI via variables de entorno.",
    details: [
      "API key en archivo .env",
      "python-dotenv para carga segura",
      ".env excluido del repositorio",
      "Validación de OPENAI_API_KEY en main.py"
    ],
    evidence: ".env.example presente; load_dotenv() en main.py"
  },
  {
    num: 3, title: "MVP técnico básico", status: "done", icon: "🚀",
    summary: "Flujo completo MP3 → transcript → Markdown validado.",
    details: [
      "MP3 detectado en input/",
      "Transcripción con OpenAI Whisper",
      "Análisis del contenido con GPT",
      "Markdown guardado en output/"
    ],
    evidence: "output/ contiene archivos _transcript.txt y _analysis.md"
  },
  {
    num: 4, title: "Documentación", status: "done", icon: "📚",
    summary: "Visión, decisiones y roadmap documentados.",
    details: [
      "docs/product_spec.md (especificación funcional)",
      "docs/technical_spec.md (arquitectura)",
      "docs/roadmap.md (fases del proyecto)",
      "docs/decisions_log.md (registro de decisiones)"
    ],
    evidence: "Carpeta docs/ con 5 archivos Markdown"
  },
  {
    num: 5, title: "Refactor a servicios", status: "done", icon: "⚙️",
    summary: "Lógica extraída de main.py a módulos de servicio.",
    details: [
      "services/file_service.py",
      "services/markdown_service.py",
      "services/transcription_service.py",
      "services/analysis_service.py"
    ],
    evidence: "file_service.py y markdown_service.py confirmados en services/"
  },
  {
    num: 6, title: "Servicios intercambiables", status: "done", icon: "🔄",
    summary: "Interfaces que permiten cambiar de proveedor sin reescribir el flujo.",
    details: [
      "services/transcription/base.py (interfaz base)",
      "services/analysis/base.py (interfaz base)",
      "services/transcription/openai_transcription.py",
      "services/analysis/openai_analysis.py"
    ],
    evidence: "Subdirectorios transcription/ y analysis/ con base.py confirmados"
  },
  {
    num: 7, title: "Primera arquitectura de agentes", status: "done", icon: "🤖",
    summary: "Agentes simples que coordinan el pipeline.",
    details: [
      "agents/orchestrator_agent.py",
      "agents/transcription_agent.py",
      "agents/analysis_agent.py",
      "agents/markdown_agent.py",
      "agents/archive_agent.py"
    ],
    evidence: "Carpeta agents/ con los 5 agentes confirmados"
  },
  {
    num: 8, title: "Archive Agent", status: "done", icon: "📦",
    summary: "Los MP3 procesados se mueven automáticamente a processed/.",
    details: [
      "ArchiveAgent crea processed/ si no existe",
      "Mueve el MP3 solo si el proceso fue exitoso",
      "Evita sobreescribir archivos duplicados (timestamp)",
      "Integrado en OrchestratorAgent"
    ],
    evidence: "archive_agent.py implementado con shutil.move; orchestrator lo usa"
  },
  {
    num: 9, title: "Mejorar CLAUDE.md", status: "done", icon: "📋",
    summary: "Reglas permanentes de trabajo para Claude Code.",
    details: [
      "Código simple y claro, sin sobre-ingeniería",
      "Comentarios breves donde ayuden",
      "No implementar múltiples cambios grandes a la vez",
      "Explicar plan antes de modificar código"
    ],
    evidence: "CLAUDE.md contiene sección Coding Guidelines completa"
  },
  {
    num: 10, title: "Agentes con prompts propios", status: "current", icon: "✍️",
    summary: "Dar instrucciones específicas a cada agente via archivos de prompts.",
    details: [
      "prompts/orchestrator_agent.md",
      "prompts/analysis_agent.md",
      "prompts/task_extraction_agent.md",
      "prompts/meeting_summary_agent.md",
      "prompts/markdown_writer_agent.md"
    ],
    evidence: "prompts/ existe pero solo tiene .gitkeep — carpeta vacía"
  },
  {
    num: 11, title: "Clasificación real por tipo", status: "pending", icon: "🏷️",
    summary: "Clasificar cada entrada en 6 categorías oficiales.",
    details: [
      "Categorías: Idea, Reunión, Tarea, Recordatorio",
      "Categorías: Proyecto, Nota general",
      "Categoría principal + elementos secundarios",
      "Una reunión puede generar tareas, ideas y recordatorios"
    ],
    evidence: ""
  },
  {
    num: 12, title: "Salidas Markdown V1", status: "pending", icon: "📂",
    summary: "Base de conocimiento organizada en carpetas y archivos Markdown.",
    details: [
      "Knowledge_Base/Ideas/ideas.md (acumulativo)",
      "Knowledge_Base/Tasks/tasks.md (acumulativo)",
      "Knowledge_Base/Meetings/YYYY-MM-DD_reunion.md (individual)",
      "Knowledge_Base/Projects/projects.md (maestro)"
    ],
    evidence: ""
  },
  {
    num: 13, title: "Integración Google Tasks", status: "pending", icon: "✅",
    summary: "Crear tareas reales en Google Tasks cuando hay acciones pendientes.",
    details: [
      "Si acción tiene fecha pero no hora → Google Task",
      "Registro también en tasks.md",
      "Integración con Google Tasks API"
    ],
    evidence: ""
  },
  {
    num: 14, title: "Integración Google Calendar", status: "pending", icon: "📅",
    summary: "Crear eventos cuando hay fecha y hora claras.",
    details: [
      "Fecha + hora → Google Calendar event",
      "Solo fecha → Google Tasks",
      "Ambiguo → Markdown 'requiere revisión'"
    ],
    evidence: ""
  },
  {
    num: 15, title: "Integración Google Drive", status: "pending", icon: "☁️",
    summary: "Procesar archivos directamente desde Google Drive.",
    details: [
      "Leer desde Drive/Second_Brain/Inbox",
      "Escribir Knowledge Base en Google Drive",
      "Mover procesados a carpeta Processed en Drive"
    ],
    evidence: ""
  },
  {
    num: 16, title: "Migración a LangGraph", status: "pending", icon: "🕸️",
    summary: "Convertir el pipeline de agentes en un grafo formal.",
    details: [
      "intake_node → transcription_node → classification_node",
      "task_node → calendar_node → markdown_node → archive_node",
      "Mejor control de flujo y manejo de estados"
    ],
    evidence: ""
  },
  {
    num: 17, title: "Cloud Run + Scheduler", status: "pending", icon: "🌐",
    summary: "Ejecución automática en la nube sin depender del PC.",
    details: [
      "Contenerizar con Docker",
      "Deploy en Google Cloud Run",
      "Cloud Scheduler para ejecuciones periódicas",
      "Logs y monitoreo básico"
    ],
    evidence: ""
  },
  {
    num: 18, title: "Agente consultable V2", status: "pending", icon: "💬",
    summary: "Consultar la base de conocimiento con lenguaje natural.",
    details: [
      "¿Qué pendientes tengo para mañana?",
      "¿Qué ideas tuve esta semana?",
      "Indexación semántica de Markdown",
      "Posible base vectorial"
    ],
    evidence: ""
  },
  {
    num: 19, title: "Interfaz conversacional V3", status: "pending", icon: "📱",
    summary: "Interacción natural desde múltiples canales.",
    details: [
      "Chat web propio",
      "Integración con Telegram",
      "Integración con WhatsApp",
      "App móvil (futuro)"
    ],
    evidence: ""
  }
];

/* ─── Helpers ───────────────────────────────────────── */
const statusLabel = { done: "✅ Completado", current: "🔄 En progreso", pending: "⏳ Pendiente" };

function countByStatus(status) {
  return ROADMAP.filter(s => s.status === status).length;
}

/* ─── Build Stars ───────────────────────────────────── */
function buildStars() {
  const container = document.getElementById('stars');
  if (!container) return;
  const count = 90;
  for (let i = 0; i < count; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const size = Math.random() * 2.2 + 0.5;
    s.style.cssText = `
      width: ${size}px; height: ${size}px;
      top: ${Math.random() * 100}%;
      left: ${Math.random() * 100}%;
      --op: ${(Math.random() * 0.5 + 0.15).toFixed(2)};
      --dur: ${(Math.random() * 3 + 2).toFixed(1)}s;
      --delay: ${(Math.random() * 4).toFixed(1)}s;
    `;
    container.appendChild(s);
  }
}

/* ─── Render Steps ──────────────────────────────────── */
function renderSteps() {
  const container = document.getElementById('steps-list');
  if (!container) return;

  ROADMAP.forEach((step, idx) => {
    const side = idx % 2 === 0 ? 'left' : 'right';
    const row = document.createElement('div');
    row.className = 'step';
    row.setAttribute('data-step', step.num);
    row.setAttribute('data-status', step.status);
    row.setAttribute('data-side', side);

    const detailItems = step.details.map(d => `<li>${d}</li>`).join('');
    const evidenceHtml = step.evidence
      ? `<div class="card-evidence"><strong>Evidencia:</strong> ${step.evidence}</div>`
      : '';

    const cardHtml = `
      <div class="step-card ${step.status}" data-card="${step.num}">
        <div class="card-header">
          <span class="card-num-badge">Parada #${step.num}</span>
          <span class="card-status-badge ${step.status}">${statusLabel[step.status]}</span>
        </div>
        <div class="card-title-row">
          <span class="card-icon">${step.icon}</span>
          <span class="card-title">${step.title}</span>
        </div>
        <div class="card-summary">${step.summary}</div>
        <div class="card-expand-btn" data-toggle="${step.num}">
          <span>Ver detalles</span>
          <em class="expand-arrow">▾</em>
        </div>
        <div class="card-details">
          <div class="card-details-inner">
            <ul>${detailItems}</ul>
            ${evidenceHtml}
          </div>
        </div>
      </div>
    `;

    const dotHtml = `
      <div class="step-dot-col">
        <div class="step-dot ${step.status}" title="Parada #${step.num}">
          ${step.status === 'done' ? '✓' : step.num}
        </div>
      </div>
    `;

    const spacerHtml = `<div class="step-spacer"></div>`;

    if (side === 'left') {
      row.innerHTML = cardHtml + dotHtml + spacerHtml;
    } else {
      row.innerHTML = spacerHtml + dotHtml + cardHtml;
    }

    container.appendChild(row);
  });
}

/* ─── Update Stats ──────────────────────────────────── */
function updateStats() {
  const done    = countByStatus('done');
  const pending = countByStatus('pending');
  const total   = ROADMAP.length;
  const pct     = Math.round((done / total) * 100);

  const el = n => document.getElementById(n);

  if (el('count-done'))    el('count-done').textContent    = done;
  if (el('count-pending')) el('count-pending').textContent = pending;

  // Progress gauge
  if (el('gauge-fill')) {
    setTimeout(() => {
      el('gauge-fill').style.width = pct + '%';
      if (el('gauge-car')) el('gauge-car').style.left = pct + '%';
      if (el('gauge-pct')) el('gauge-pct').textContent = pct + '%';
    }, 600);
  }

  // Banner
  const currentStep = ROADMAP.find(s => s.status === 'current');
  const nextStep    = ROADMAP.find((s, i) => i > ROADMAP.indexOf(currentStep) && s.status === 'pending');
  if (el('banner-title') && currentStep) el('banner-title').textContent = `#${currentStep.num} ${currentStep.title}`;
  if (el('banner-next') && nextStep)     el('banner-next').textContent  = `#${nextStep.num} ${nextStep.title}`;
}

/* ─── Animate Car Down the Road ─────────────────────── */
function animateCar() {
  const car       = document.getElementById('road-car');
  const tlWrap    = document.getElementById('timeline-wrap');
  const currentEl = document.querySelector('[data-step="10"] .step-dot');

  if (!car || !tlWrap || !currentEl) return;

  // Calculate Y relative to timeline-wrap using offsetTop traversal
  function getRelativeTop(el, ancestor) {
    let top = 0;
    while (el && el !== ancestor) {
      top += el.offsetTop;
      el = el.offsetParent;
    }
    return top;
  }

  const dotY    = getRelativeTop(currentEl, tlWrap);
  const carH    = car.offsetHeight;
  const targetY = dotY - carH / 2;

  // Car starts at top of timeline
  car.style.top = '40px';

  // After 900ms: scroll to current step, then animate car
  setTimeout(() => {
    const target10 = document.querySelector('[data-step="10"]');
    if (target10) {
      target10.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    // Small extra delay so the page scrolls before car moves
    setTimeout(() => {
      car.style.top = Math.max(targetY, 20) + 'px';
    }, 300);
  }, 900);
}

/* ─── Expand / Collapse Cards ───────────────────────── */
function initToggle() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-toggle]');
    if (!btn) return;
    const num  = btn.getAttribute('data-toggle');
    const card = document.querySelector(`.step-card[data-card="${num}"]`);
    if (!card) return;
    card.classList.toggle('open');
    const label = btn.querySelector('span');
    if (label) label.textContent = card.classList.contains('open') ? 'Ocultar detalles' : 'Ver detalles';
  });
}

/* ─── Scroll Reveal for Steps ───────────────────────── */
function initReveal() {
  const obs = new IntersectionObserver(
    entries => entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); }
    }),
    { threshold: 0.08, rootMargin: '0px 0px -30px 0px' }
  );
  document.querySelectorAll('.step').forEach((el, i) => {
    el.style.transitionDelay = (i * 0.04) + 's';
    obs.observe(el);
  });
}

/* ─── Auto-open current step card ───────────────────── */
function openCurrentCard() {
  const currentCard = document.querySelector('.step-card.current');
  if (currentCard) {
    currentCard.classList.add('open');
    const btn = currentCard.querySelector('[data-toggle] span');
    if (btn) btn.textContent = 'Ocultar detalles';
  }
}

/* ─── Footer date ───────────────────────────────────── */
function setDate() {
  const el = document.getElementById('footer-date');
  if (el) el.textContent = new Date().toLocaleDateString('es-MX', { year: 'numeric', month: 'long', day: 'numeric' });
}

/* ─── Init ──────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  buildStars();
  renderSteps();
  updateStats();
  openCurrentCard();
  initToggle();
  initReveal();
  setDate();

  // Car animation after a tick so layout is calculated
  requestAnimationFrame(() => {
    setTimeout(animateCar, 200);
  });
});
