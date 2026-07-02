/**
 * HelpOS Chat.js
 * Chat panel: message rendering, streaming, dual-mode output.
 */

// ── State ─────────────────────────────────────────────────
const conversationHistory = [];

// ── DOM refs ──────────────────────────────────────────────
const msgList    = document.getElementById('chat-messages');
const emptyState = document.getElementById('chat-empty');
const chatInput  = document.getElementById('chat-input');
const sendBtn    = document.getElementById('chat-send-btn');

// ── Helpers ───────────────────────────────────────────────

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function renderMarkdown(text) {
  if (typeof marked !== 'undefined') {
    return marked.parse(text, { breaks: true });
  }
  // Fallback: simple newline → <br>
  return escapeHtml(text).replace(/\n/g, '<br>');
}

function formatNumber(val) {
  if (typeof val !== 'number') return String(val);
  // Scientific notation for very large/small
  if (Math.abs(val) >= 1e15 || (Math.abs(val) < 1e-3 && val !== 0)) {
    return val.toExponential(4);
  }
  // Round to 4 decimals max
  return parseFloat(val.toPrecision(6)).toString();
}

function toolDisplayName(tool) {
  const names = {
    molar_mass:           'Molar Mass',
    convert_grams_moles:  'Grams ↔ Moles',
    stp_conversion:       'STP Conversion',
    avogadro_calculation: 'Avogadro Calculation',
    math_solve:           'Math Expression',
  };
  return names[tool] || tool;
}

function buildDeterministicCard(data) {
  const { tool, args = {}, result = {} } = data;
  const value = result.result ?? result.molar_mass ?? result.expression ?? '—';
  const unit  = result.unit || result.unit_label || '';
  const displayVal = typeof value === 'number' ? formatNumber(value) : String(value);

  // Build arg pills
  const argPills = Object.entries(args).map(([k, v]) =>
    `<div class="det-input-item">${k}: <span>${escapeHtml(String(v))}</span></div>`
  ).join('');

  return `
    <div class="det-result-card">
      <div class="det-header">
        <div class="det-tool-name">${escapeHtml(toolDisplayName(tool))}</div>
        <span class="mode-badge deterministic">⚡ Exact</span>
      </div>
      <div class="det-value">${escapeHtml(displayVal)}</div>
      ${unit ? `<div class="det-unit">${escapeHtml(unit)}</div>` : ''}
      ${argPills ? `<div class="det-inputs">${argPills}</div>` : ''}
    </div>`;
}

// ── Message rendering ─────────────────────────────────────

function appendMessage(role, contentHtml, extraClass = '') {
  // Hide empty state on first message
  if (emptyState) emptyState.style.display = 'none';

  const wrap = document.createElement('div');
  wrap.className = `chat-message ${role} ${extraClass}`.trim();

  const roleName = role === 'user' ? 'You' : 'HelpOS';

  wrap.innerHTML = `
    <div class="message-meta">
      <span class="message-role">${roleName}</span>
    </div>
    <div class="message-bubble">${contentHtml}</div>`;

  msgList.appendChild(wrap);
  scrollToBottom();
  return wrap.querySelector('.message-bubble');
}

function appendTypingIndicator() {
  if (emptyState) emptyState.style.display = 'none';
  const wrap = document.createElement('div');
  wrap.className = 'chat-message assistant';
  wrap.id = 'typing-indicator-wrap';
  wrap.innerHTML = `
    <div class="message-meta"><span class="message-role">HelpOS</span></div>
    <div class="typing-indicator">
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    </div>`;
  msgList.appendChild(wrap);
  scrollToBottom();
  return wrap;
}

function removeTypingIndicator() {
  const el = document.getElementById('typing-indicator-wrap');
  if (el) el.remove();
}

function scrollToBottom() {
  msgList.scrollTop = msgList.scrollHeight;
}

// ── API call ──────────────────────────────────────────────

async function sendMessage(text) {
  const trimmed = text.trim();
  if (!trimmed) return;

  // Disable input while processing
  setInputBusy(true);

  // Add to conversation history
  conversationHistory.push({ role: 'user', content: trimmed });

  // Render user message
  appendMessage('user', escapeHtml(trimmed).replace(/\n/g, '<br>'));

  // Show typing
  appendTypingIndicator();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: conversationHistory,
        stream: false
      })
    });

    removeTypingIndicator();

    if (!res.ok) {
      const errData = await res.json().catch(() => ({}));
      appendMessage('assistant',
        `<span style="color:var(--accent-red);">⚠ Error ${res.status}: ${escapeHtml(errData.detail || 'Unknown error')}</span>`
      );
      setInputBusy(false);
      return;
    }

    const data = await res.json();

    if (data.mode === 'deterministic') {
      // Mode B — render result card
      const cardHtml = buildDeterministicCard(data);
      const bubble = appendMessage('assistant', cardHtml);

      // Add to history as textual summary
      const val = data.result?.result ?? data.result?.molar_mass ?? '';
      const unit = data.result?.unit || '';
      conversationHistory.push({
        role: 'assistant',
        content: `[${toolDisplayName(data.tool)} result: ${val} ${unit}]`
      });

    } else if (data.mode === 'reasoning') {
      // Mode A — render markdown
      const md = renderMarkdown(data.content || '');
      appendMessage('assistant', md);

      conversationHistory.push({ role: 'assistant', content: data.content || '' });

    } else if (data.mode === 'error') {
      appendMessage('assistant',
        `<span style="color:var(--accent-red);">⚠ ${escapeHtml(data.detail || 'An error occurred.')}</span>`
      );
    } else {
      // Fallback — try to display whatever came back
      appendMessage('assistant', `<pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>`);
    }

  } catch (err) {
    removeTypingIndicator();
    appendMessage('assistant',
      `<span style="color:var(--accent-red);">⚠ Network error: ${escapeHtml(err.message)}. Is the HelpOS server running?</span>`
    );
  }

  setInputBusy(false);
  chatInput.focus();
}

// ── Input helpers ─────────────────────────────────────────

function setInputBusy(busy) {
  chatInput.disabled = busy;
  sendBtn.disabled   = busy;
}

function autoResizeTextarea() {
  chatInput.style.height = 'auto';
  chatInput.style.height = Math.min(chatInput.scrollHeight, 160) + 'px';
}

// ── Event wiring ──────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  // Send button
  sendBtn.addEventListener('click', () => {
    sendMessage(chatInput.value);
    chatInput.value = '';
    autoResizeTextarea();
  });

  // Enter to send, Shift+Enter for newline
  chatInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(chatInput.value);
      chatInput.value = '';
      autoResizeTextarea();
    }
  });

  // Auto-resize textarea
  chatInput.addEventListener('input', autoResizeTextarea);

  // Suggestion chips
  document.querySelectorAll('.suggestion-chip[data-msg]').forEach(chip => {
    chip.addEventListener('click', () => {
      chatInput.value = chip.dataset.msg;
      autoResizeTextarea();
      chatInput.focus();
    });
  });
});
