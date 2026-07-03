/**
 * HelpOS App.js
 * Navigation router, panel switching, keyboard shortcuts,
 * and Ollama status polling.
 */

const PANEL_META = {
  chat:      { title: 'Chat',          subtitle: 'Dual-mode AI — Reasoning & Deterministic' },
  chemistry: { title: 'Chemistry',     subtitle: 'Exact calculations from the CDE periodic table' },
  math:      { title: 'Math Solver',   subtitle: 'Deterministic expression evaluation' },
  utilities: { title: 'Utilities',     subtitle: 'Local client-side tools — no API calls' },
  study:     { title: 'Study Tools',   subtitle: 'Flashcards, notes & Pomodoro' },
  documents: { title: 'Docs',          subtitle: 'AI summarization and study questions' },
};

// ── Panel Router ──────────────────────────────────────────

function navigateTo(panelKey) {
  if (!PANEL_META[panelKey]) return;

  // Update panels
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const target = document.getElementById(`panel-${panelKey}`);
  if (target) target.classList.add('active');

  // Update nav items
  document.querySelectorAll('.nav-item').forEach(n => {
    n.classList.remove('active');
    n.removeAttribute('aria-current');
  });
  const navItem = document.getElementById(`nav-${panelKey}`);
  if (navItem) {
    navItem.classList.add('active');
    navItem.setAttribute('aria-current', 'page');
  }

  // Update topbar
  const meta = PANEL_META[panelKey];
  document.getElementById('topbar-title').textContent = meta.title;
  document.getElementById('topbar-subtitle').textContent = meta.subtitle;

  // Store active panel
  window._activePanel = panelKey;
}

// ── Nav event wiring ──────────────────────────────────────

function wireNavigation() {
  document.querySelectorAll('.nav-item[data-panel]').forEach(item => {
    const panelKey = item.dataset.panel;
    item.addEventListener('click', () => navigateTo(panelKey));
    item.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); navigateTo(panelKey); }
    });
  });
}

// ── Keyboard Shortcuts ─────────────────────────────────────

function wireKeyboardShortcuts() {
  document.addEventListener('keydown', e => {
    // Skip if user is typing in an input
    const tag = document.activeElement?.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;

    // Number keys 1-6 switch panels
    const panelOrder = ['chat', 'chemistry', 'math', 'study', 'documents', 'utilities'];
    const num = parseInt(e.key, 10);
    if (num >= 1 && num <= panelOrder.length) {
      navigateTo(panelOrder[num - 1]);
    }
  });
}

// ── Ollama Status Polling ──────────────────────────────────

const statusDot  = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');

async function checkOllamaStatus() {
  statusDot.className  = 'status-dot checking';
  statusText.textContent = 'Checking…';
  try {
    const res  = await fetch('/api/health', { signal: AbortSignal.timeout(3000) });
    const data = await res.json();
    if (data?.ollama?.connected) {
      statusDot.className    = 'status-dot online';
      const model = data.ollama.configured_model || 'Ollama';
      statusText.textContent = model;
    } else {
      statusDot.className    = 'status-dot offline';
      statusText.textContent = 'Ollama offline';
    }
  } catch {
    statusDot.className    = 'status-dot offline';
    statusText.textContent = 'Cannot reach server';
  }
}

// ── Init ──────────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  wireNavigation();
  wireKeyboardShortcuts();
  navigateTo('chat');
  checkOllamaStatus();
  setInterval(checkOllamaStatus, 15_000);
});
