/** HelpOS Study.js — local flashcards, notes, pomodoro, and AI docs. */
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
  function renderNotes() {
    if (!preview) return;
    preview.innerHTML = notes?.value.trim()
      ? renderMarkdown(notes.value)
      : '<span class="text-muted">Markdown preview appears here.</span>';
    wireCopyCodeButtons(preview);
  }
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
  const summaryBtn = document.getElementById('doc-summary-btn');
  const questionsBtn = document.getElementById('doc-questions-btn');

  async function runDocAction(action) {
    const text = docInput?.value.trim();
    if (!text) {
      docOutput.className = 'result-card empty-state';
      docOutput.textContent = 'Paste document text first.';
      return;
    }

    const activeBtn = action === 'summary' ? summaryBtn : questionsBtn;
    const otherBtn = action === 'summary' ? questionsBtn : summaryBtn;
    activeBtn.disabled = true;
    otherBtn.disabled = true;
    activeBtn.textContent = action === 'summary' ? 'Summarizing…' : 'Generating…';
    docOutput.className = 'result-card markdown-output';
    docOutput.innerHTML = '<div style="color:var(--text-muted); font-size:13px;">Working with local AI…</div>';

    try {
      const res = await fetch('/api/docs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action: action === 'summary' ? 'summary' : 'questions',
          text,
        }),
      });

      const data = await res.json();
      if (!res.ok) {
        docOutput.innerHTML = `<p style="color:var(--accent-red);">⚠ ${escapeHtml(data.detail || 'Request failed.')}</p>`;
        return;
      }

      if (data.mode === 'reasoning') {
        docOutput.innerHTML = renderMarkdown(data.content || '');
        wireCopyCodeButtons(docOutput);
      } else if (data.mode === 'error') {
        docOutput.innerHTML = `<p style="color:var(--accent-red);">⚠ ${escapeHtml(data.detail || 'An error occurred.')}</p>`;
      } else {
        docOutput.innerHTML = `<p style="color:var(--accent-red);">⚠ Unexpected response from AI.</p>`;
      }
    } catch (err) {
      docOutput.innerHTML = `<p style="color:var(--accent-red);">⚠ Network error: ${escapeHtml(err.message)}</p>`;
    } finally {
      activeBtn.disabled = false;
      otherBtn.disabled = false;
      activeBtn.textContent = action === 'summary' ? 'Summarize' : 'Make study questions';
    }
  }

  summaryBtn?.addEventListener('click', () => runDocAction('summary'));
  questionsBtn?.addEventListener('click', () => runDocAction('questions'));
});
