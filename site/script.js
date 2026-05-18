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
    num: 10, title: "Agentes con prompts propios", status: "done", icon: "✍️",
    summary: "Cada agente carga sus instrucciones desde un archivo Markdown en prompts/.",
    details: [
      "prompts/orchestrator_agent.md",
      "prompts/analysis_agent.md",
      "prompts/transcription_agent.md",
      "prompts/markdown_agent.md",
      "prompts/archive_agent.md"
    ],
    evidence: "AnalysisAgent carga analysis_agent.md via prompt_loader.py al inicializarse"
  },
  {
    num: 11, title: "Clasificación real por tipo", status: "done", icon: "🏷️",
    summary: "GPT clasifica en 6 categorías y devuelve JSON estructurado con todos los campos.",
    details: [
      "6 categorías: Idea, Reunión, Tarea, Recordatorio, Proyecto, Nota general",
      "response_format=json_object garantiza JSON válido",
      "AnalysisResult con 15 campos incluyendo participants, decisions, actions_for_me/others",
      "Fechas relativas preservadas tal como se dijeron — sin inventar fechas"
    ],
    evidence: "services/analysis/analysis_result.py + openai_analysis.py verificados en pruebas reales"
  },
  {
    num: 115, title: "Procesamiento múltiple de archivos", status: "done", icon: "📦",
    summary: "El sistema procesa todos los MP3 de input/ en una sola ejecución.",
    details: [
      "find_all_mp3() devuelve lista ordenada de todos los archivos",
      "OrchestratorAgent itera con _process_one() por archivo",
      "Error en un archivo no detiene los demás",
      "Resumen final: Total | OK | Failed"
    ],
    evidence: "Verificado con 5-6 MP3 simultáneos: 6/6 OK en prueba real"
  },
  {
    num: 12, title: "Knowledge Base Markdown V1", status: "done", icon: "📂",
    summary: "Información organizada en carpetas por categoría con enrutado secundario.",
    details: [
      "Ideas, Tasks, Reminders, Projects: archivos acumulativos",
      "Meetings, General_Notes: archivos individuales por fecha",
      "Tareas de reuniones también llegan a tasks.md (enrutado secundario)",
      "Reuniones con secciones: Participantes, Decisiones, Acciones, Riesgos, Próximos pasos",
      "Tags obligatorios en todas las salidas (mínimo 2)"
    ],
    evidence: "Knowledge_Base/ generada y verificada con 5 MP3 reales: Ideas, Tasks, Meetings, Reminders correctos"
  },
  {
    num: 13, title: "Integración Google Tasks", status: "done", icon: "✅",
    summary: "Tareas reales en Google Tasks con prefijo de proyecto y due date automático.",
    details: [
      "Tarea sin fecha → Google Task con due date +7 días",
      "Tarea con fecha pero sin hora → Google Task con due date exacto",
      "Recordatorio con fecha + hora → reservado para Calendar",
      "Prefijo [Proyecto] en título cuando hay proyecto asignado",
      "Deduplicación via created_tasks.json"
    ],
    evidence: "Verificado en prueba real: tarea SAT creada con due date mañana en lista 'Second Brain Agent'"
  },
  {
    num: 14, title: "Integración Google Calendar", status: "done", icon: "📅",
    summary: "Eventos reales en Google Calendar cuando hay fecha y hora claras.",
    details: [
      "Recordatorio con fecha + hora → evento en Calendar (1 hora duración)",
      "Título limpio desde result.title, no del texto crudo",
      "Timezone configurable via .env (default: America/Mexico_City)",
      "Token separado de Tasks: token_calendar.json",
      "Deduplicación via created_events.json"
    ],
    evidence: "Verificado: evento 'Recordatorio de cita para renovación de visa' creado el 16 mayo 19:00"
  },
  {
    num: 15, title: "Integración Google Drive", status: "done", icon: "☁️",
    summary: "Drive como capa de I/O: Inbox → proceso local → KB en Drive → Processed.",
    details: [
      "DriveAgent descarga MP3s de Drive Inbox a input/ local",
      "Pipeline procesa normalmente sin cambios",
      "KB files se suben a Drive tras cada procesamiento",
      "Upload actualiza archivo existente en Drive (no duplica)",
      "MP3 original se mueve a Drive Processed al finalizar",
      "Sistema sigue funcionando sin Drive si no hay IDs configurados"
    ],
    evidence: "Verificado: 2 MP3s descargados de Drive, KB subida, archivos movidos a Processed"
  },
  {
    num: 16, title: "Migración a LangGraph", status: "done", icon: "🕸️",
    summary: "Pipeline orquestado por un StateGraph de 9 nodos con estado compartido.",
    details: [
      "pipeline/state.py — PipelineState TypedDict compartido entre nodos",
      "pipeline/nodes.py — 9 funciones nodo que envuelven agentes existentes",
      "pipeline/graph.py — StateGraph lineal compilado una vez al inicio",
      "Agentes existentes sin cambios — LangGraph solo orquesta",
      "Error en cualquier nodo detiene el pipeline, MP3 no se mueve"
    ],
    evidence: "Verificado: pipeline completo con LangGraph, resultado idéntico al anterior"
  },
  {
    num: 17, title: "Cloud Run + Scheduler", status: "pending", icon: "🌐",
    summary: "Ejecución automática en la nube sin depender del PC. (Pausado — se retoma después del paso 20)",
    details: [
      "Contenerizar con Docker",
      "Deploy en Google Cloud Run",
      "Cloud Scheduler para ejecuciones periódicas",
      "Logs y monitoreo básico"
    ],
    evidence: ""
  },
  {
    num: 18, title: "Agente consultable RAG", status: "done", icon: "🔍",
    summary: "Chat conversacional con búsqueda semántica en la Knowledge Base + captura por texto.",
    details: [
      "ChromaDB como vector store local persistente",
      "OpenAI text-embedding-3-small para embeddings (~$0.02/M tokens)",
      "Modo QUERY: búsqueda semántica, responde solo con info de la KB",
      "Modo CAPTURE: texto nuevo → AnalysisAgent → KB + Tasks + Calendar + re-indexado",
      "Clasificador de intención via GPT-4o-mini (QUERY vs CAPTURE)",
      "Memoria de conversación dentro de la sesión (últimos 10 mensajes)",
      "chat.py como punto de entrada independiente"
    ],
    evidence: "chat.py funcional: indexa 15+ chunks, clasifica intención correctamente, captura crea MD y re-indexa"
  },
  {
    num: 19, title: "Refactor MessageHandler", status: "done", icon: "🔧",
    summary: "process_message() como función central canal-agnóstica reutilizable por cualquier entrypoint.",
    details: [
      "core/message_handler.py — MessageHandler con process_message() y process_voice()",
      "core/agent_factory.py — build_message_handler() inicializa todos los agentes",
      "chat.py simplificado a solo el loop de terminal",
      "Cualquier canal (Telegram, app web, API) llama a process_message() sin conocer el pipeline"
    ],
    evidence: "chat.py reducido a ~40 líneas; MessageHandler reutilizado por telegram_bot.py sin duplicar lógica"
  },
  {
    num: 20, title: "Telegram — canal completo", status: "done", icon: "✈️",
    summary: "Bot de Telegram que captura audios y texto, y responde consultas desde el teléfono.",
    details: [
      "telegram_bot.py en modo polling (sin URL pública requerida)",
      "Texto → classify_intent (GPT) → QUERY o CAPTURE",
      "Nota de voz (.ogg) → Whisper → AnalysisAgent → KB + Tasks + Calendar",
      "Whitelist de usuario via TELEGRAM_ALLOWED_USER_ID (seguridad)",
      "Comandos /start y /reset",
      "Indicador 'escribiendo...' mientras procesa"
    ],
    evidence: "Bot funcional con token activo; whitelist configurada con user ID del propietario"
  },
  {
    num: 17, title: "Cloud Run + Scheduler", status: "current", icon: "🌐",
    summary: "Próximo paso: ejecución automática en la nube sin depender del PC.",
    details: [
      "Contenerizar con Docker",
      "Deploy en Google Cloud Run",
      "Cloud Scheduler para ejecuciones periódicas",
      "Telegram webhook en lugar de polling",
      "Logs y monitoreo básico"
    ],
    evidence: ""
  },
  {
    num: 21, title: "App propia — dashboard central", status: "pending", icon: "🚀",
    summary: "Nuevo proyecto: app con chat IA + vistas de ideas, tareas, calendario y reuniones.",
    details: [
      "Backend FastAPI usando MessageHandler existente",
      "Dashboard web: lista de ideas, tareas pendientes, resúmenes de reuniones",
      "Vista de calendario integrada",
      "Chat IA embebido en la app",
      "Proyecto separado — reutiliza core/ del agente actual"
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
  const currentStep = ROADMAP.find(s => s.status === 'current');
  const currentNum  = currentStep ? currentStep.num : 17;
  const currentEl   = document.querySelector(`[data-step="${currentNum}"] .step-dot`);

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
    const targetEl = document.querySelector(`[data-step="${currentNum}"]`);
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
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
