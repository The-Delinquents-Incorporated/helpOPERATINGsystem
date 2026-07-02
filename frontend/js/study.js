/** HelpOS Study.js — local flashcards, notes, pomodoro, document helpers. */
document.addEventListener('DOMContentLoaded', () => {
  const cards = JSON.parse(localStorage.getItem('helpos.flashcards') || '[]');
  let cardIndex = 0;
  let showingBack = false;
  const front = document.getElementById('flash-front');
  const back = document.getElementById('flash-back');
  const stage = document.getElementById('flashcard-stage');

  function saveCards() { localStorage.setItem('helpos.flashcards', JSON.stringify(cards)); }
  function renderCard() {
    if (!stage) return;
    if (!cards.length) { stage.className = 'study-stage empty-state'; stage.textContent = 'No cards yet. Add one to start reviewing.'; return; }
    const card = cards[cardIndex % cards.length];
    stage.className = 'study-stage';
    stage.innerHTML = `<div class="study-stage-label">${showingBack ? 'Back' : 'Front'} · ${cardIndex + 1}/${cards.length}</div><div>${escapeHtml(showingBack ? card.back : card.front)}</div><div class="flex gap-2 mt-3"><button class="btn btn-primary btn-sm" id="flash-flip-btn">Flip</button><button class="btn btn-ghost btn-sm" id="flash-next-btn">Next</button></div>`;
    document.getElementById('flash-flip-btn')?.addEventListener('click', () => { showingBack = !showingBack; renderCard(); });
    document.getElementById('flash-next-btn')?.addEventListener('click', () => { showingBack = false; cardIndex = (cardIndex + 1) % cards.length; renderCard(); });
  }
  document.getElementById('flash-add-btn')?.addEventListener('click', () => {
    if (!front.value.trim() || !back.value.trim()) return;
    cards.push({ front: front.value.trim(), back: back.value.trim() });
    front.value = ''; back.value = ''; saveCards(); renderCard();
  });
  renderCard();

  const notes = document.getElementById('notes-input');
  const preview = document.getElementById('notes-preview');
  function renderNotes() { if (preview) preview.innerHTML = notes?.value.trim() ? renderMarkdownSafe(notes.value) : '<span class="text-muted">Markdown preview appears here.</span>'; }
  if (notes) { notes.value = localStorage.getItem('helpos.notes') || ''; notes.addEventListener('input', renderNotes); renderNotes(); }
  document.getElementById('notes-save-btn')?.addEventListener('click', () => localStorage.setItem('helpos.notes', notes.value));
  document.getElementById('notes-clear-btn')?.addEventListener('click', () => { notes.value = ''; localStorage.removeItem('helpos.notes'); renderNotes(); });

  let seconds = 25 * 60; let interval = null;
  const face = document.getElementById('timer-face');
  function renderTimer() { if (face) face.textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`; }
  document.getElementById('timer-start-btn')?.addEventListener('click', e => {
    if (interval) { clearInterval(interval); interval = null; e.currentTarget.textContent = 'Start'; return; }
    e.currentTarget.textContent = 'Pause';
    interval = setInterval(() => { seconds = Math.max(0, seconds - 1); renderTimer(); if (seconds === 0) { clearInterval(interval); interval = null; e.currentTarget.textContent = 'Start'; } }, 1000);
  });
  document.getElementById('timer-reset-btn')?.addEventListener('click', () => { clearInterval(interval); interval = null; seconds = 25 * 60; document.getElementById('timer-start-btn').textContent = 'Start'; renderTimer(); });

  const docInput = document.getElementById('doc-input');
  const docOutput = document.getElementById('doc-output');
  function sentences(text) { return text.replace(/\s+/g, ' ').match(/[^.!?]+[.!?]+/g) || []; }
  document.getElementById('doc-summary-btn')?.addEventListener('click', () => {
    const text = docInput.value.trim();
    if (!text) { docOutput.textContent = 'Paste document text first.'; return; }
    const summary = sentences(text).slice(0, 5).join(' ') || text.slice(0, 700);
    docOutput.innerHTML = `<div class="result-label">Extractive summary</div><p>${escapeHtml(summary)}</p>`;
  });
  document.getElementById('doc-questions-btn')?.addEventListener('click', () => {
    const words = [...new Set((docInput.value.match(/\b[A-Z][a-zA-Z]{4,}\b/g) || []).slice(0, 6))];
    const qs = (words.length ? words : ['main idea', 'evidence', 'conclusion']).map(w => `<li>What should you remember about ${escapeHtml(w)}?</li>`).join('');
    docOutput.innerHTML = `<div class="result-label">Study questions</div><ol>${qs}</ol>`;
  });
});

function escapeHtml(str) { return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
function renderMarkdownSafe(text) { return typeof marked !== 'undefined' ? marked.parse(text, { breaks: true }) : escapeHtml(text).replace(/\n/g, '<br>'); }
