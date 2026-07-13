/**
 * HelpOS Chemistry Solvers & Knowledge Base
 */

function parseCompositionInput(text) {
  const comp = {};
  // Match Element symbol followed by colon, equals, or space, then a number
  const regex = /([A-Z][a-z]?)\s*[:=\s-]\s*([\d\.]+)/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    const symbol = match[1];
    const val = parseFloat(match[2]);
    if (symbol && !isNaN(val)) {
      comp[symbol] = val;
    }
  }
  return comp;
}

// ── AI Solvers Handlers ──────────────────────────────────

async function runChemistrySolve() {
  const solverType = document.getElementById('solver-calc-type').value;
  const showWork = document.getElementById('solver-show-work').checked;
  const btn = document.getElementById('solver-calculate-btn');
  const area = document.getElementById('solver-result-area');
  const errEl = document.getElementById('solver-error');

  errEl.style.display = 'none';
  btn.disabled = true;
  btn.textContent = 'Solving…';
  area.innerHTML = '<div style="color:var(--text-muted); font-size:13px;">Solving & explaining…</div>';

  const payload = { solver_type: solverType, show_work: showWork };

  try {
    if (solverType === 'stoichiometry') {
      payload.equation = document.getElementById('stoich-equation').value.trim();
      payload.given_substance = document.getElementById('stoich-given-sub').value.trim();
      payload.given_value = parseFloat(document.getElementById('stoich-given-val').value);
      payload.given_unit = document.getElementById('stoich-given-unit').value;
      payload.target_substance = document.getElementById('stoich-target-sub').value.trim();
      payload.target_unit = document.getElementById('stoich-target-unit').value;

      if (!payload.equation || !payload.given_substance || isNaN(payload.given_value) || !payload.target_substance) {
        throw new Error('Please fill in all stoichiometry fields.');
      }
    } else if (solverType === 'empirical_molecular') {
      const compText = document.getElementById('emp-composition').value.trim();
      payload.composition = parseCompositionInput(compText);
      const molarMassRaw = parseFloat(document.getElementById('emp-molar-mass').value);
      if (!isNaN(molarMassRaw)) {
        payload.molar_mass = molarMassRaw;
      }

      if (Object.keys(payload.composition).length === 0) {
        throw new Error('Please enter valid composition data (e.g. C: 40, H: 6.7, O: 53.3).');
      }
    } else if (solverType === 'percent_composition') {
      payload.formula = document.getElementById('pct-formula').value.trim();
      if (!payload.formula) {
        throw new Error('Please enter a chemical formula.');
      }
    } else if (solverType === 'percent_error') {
      payload.theoretical = parseFloat(document.getElementById('err-theoretical').value);
      payload.experimental = parseFloat(document.getElementById('err-experimental').value);

      if (isNaN(payload.theoretical) || isNaN(payload.experimental)) {
        throw new Error('Please enter theoretical and experimental values.');
      }
    }

    const res = await fetch('/api/chemistry/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || 'Calculation or explanation failed.');
    }

    renderSolverResult(solverType, data);
  } catch (err) {
    errEl.textContent = `⚠ ${err.message}`;
    errEl.style.display = 'block';
    area.innerHTML = `<p style="color:var(--accent-red); font-size:13px;">Failed to get solution.</p>`;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Solve';
  }
}

function renderSolverResult(type, data) {
  const area = document.getElementById('solver-result-area');
  
  let resultHtml = '';
  const result = data.result;
  
  if (type === 'stoichiometry') {
    resultHtml = `
      <div class="result-card">
        <div class="result-label">Solved Value</div>
        <div class="result-value">${result.result_value}</div>
        <div class="result-unit">${result.target_unit} of ${result.target_substance}</div>
        <div class="result-meta">
          <div class="result-meta-item">Equation: <strong>${result.equation}</strong></div>
          <div class="result-meta-item">Given: <strong>${result.given_value} ${result.given_unit} of ${result.given_substance}</strong></div>
          <div class="result-meta-item">Mole Ratio: <strong>${result.mole_ratio}</strong></div>
          <div class="result-meta-item">Molar Masses: <strong>${result.given_substance}=${result.given_molar_mass} g/mol, ${result.target_substance}=${result.target_molar_mass} g/mol</strong></div>
        </div>
      </div>
    `;
  } else if (type === 'empirical_molecular') {
    resultHtml = `
      <div class="result-card">
        <div class="result-label">Empirical Formula</div>
        <div class="result-value">${result.empirical_formula}</div>
        <div class="result-unit">${result.empirical_molar_mass} g/mol</div>
        
        <div class="result-label" style="margin-top: 14px;">Molecular Formula</div>
        <div class="result-value">${result.molecular_formula}</div>
        <div class="result-unit">${result.molecular_molar_mass} g/mol</div>
        <div class="result-meta">
          <div class="result-meta-item">Molecular Multiplier: <strong>${result.molecular_multiplier}x</strong></div>
        </div>
      </div>
    `;
  } else if (type === 'percent_composition') {
    const pctList = Object.entries(result.percentages)
      .map(([sym, pct]) => `<div class="result-meta-item">${sym}: <strong>${pct}%</strong></div>`)
      .join('');
    
    resultHtml = `
      <div class="result-card">
        <div class="result-label">Molar Mass</div>
        <div class="result-value">${result.molar_mass}</div>
        <div class="result-unit">g/mol for ${result.formula}</div>
        <div class="result-meta" style="margin-top: 14px;">
          <div class="result-label" style="font-size:11px; margin-bottom: 6px;">Element Percentages</div>
          ${pctList}
        </div>
      </div>
    `;
  } else if (type === 'percent_error') {
    resultHtml = `
      <div class="result-card">
        <div class="result-label">Percent Error</div>
        <div class="result-value">${result.error_percentage}%</div>
        <div class="result-unit">${result.interpretation}</div>
        <div class="result-meta">
          <div class="result-meta-item">Theoretical: <strong>${result.theoretical}</strong></div>
          <div class="result-meta-item">Experimental: <strong>${result.experimental}</strong></div>
        </div>
      </div>
    `;
  }

  // Append markdown explanation if it exists
  let explanationHtml = '';
  if (data.show_work && data.explanation) {
    // Render with the shared markdown renderer (markdown.js) so headings,
    // lists, bold, code blocks, and chemistry sub/superscripts all display
    const formattedMarkdown = typeof renderMarkdown === 'function'
      ? renderMarkdown(data.explanation)
      : `<pre style="white-space: pre-wrap;">${escapeHtml(data.explanation)}</pre>`;
    explanationHtml = `
      <div class="explanation-box">
        <div class="explanation-title">Step-by-Step Explanation</div>
        <div class="markdown-output">${formattedMarkdown}</div>
      </div>
    `;
  }

  area.innerHTML = resultHtml + explanationHtml;
  if (typeof wireCopyCodeButtons === 'function') wireCopyCodeButtons(area);
}

// ── Knowledge Base Handlers ──────────────────────────────

async function runKBSearch() {
  const query = document.getElementById('kb-query-input').value.trim();
  const category = document.getElementById('kb-category-select').value;
  const grid = document.getElementById('kb-results-grid');
  const suggestionsBox = document.getElementById('kb-suggestions');

  grid.innerHTML = '<div style="color:var(--text-muted); padding:20px;">Searching…</div>';
  suggestionsBox.innerHTML = '';

  try {
    const url = `/api/chemistry/search-kb?query=${encodeURIComponent(query)}${category ? `&category=${category}` : ''}`;
    const res = await fetch(url);
    const data = await res.json();

    if (data.results && data.results.length > 0) {
      grid.innerHTML = data.results.map(item => renderKBCard(item)).join('');
    } else {
      grid.innerHTML = '<div style="color:var(--text-muted); padding:20px;">No matching reference items found offline.</div>';
      if (data.suggestions && data.suggestions.length > 0) {
        suggestionsBox.innerHTML = `
          <div style="font-size:12px; color:var(--text-muted); margin-bottom: 6px;">Did you mean:</div>
          <div class="suggestions-box">
            ${data.suggestions.map(s => `<div class="suggestion-chip" onclick="searchKBWithText('${s}')">${renderChemFormula(s)}</div>`).join('')}
          </div>
        `;
      }
    }
  } catch (err) {
    grid.innerHTML = `<div style="color:var(--accent-red); padding:20px;">Search error: ${err.message}</div>`;
  }
}

function searchKBWithText(text) {
  document.getElementById('kb-query-input').value = text;
  runKBSearch();
}

function renderKBCard(item) {
  const { category, data } = item;
  let title = '';
  let badge = category.replace(/_/g, ' ');
  let details = '';

  if (category === 'elements') {
    title = `${data.name} (${data.symbol})`;
    details = `
      <div>Atomic Number: <strong>${data.atomic_number}</strong></div>
      <div>Molar Mass: <strong>${data.molar_mass} g/mol</strong></div>
    `;
  } else if (category === 'compounds') {
    title = data.name;
    details = `
      <div>Formula: <strong>${renderChemFormula(data.formula)}</strong></div>
      <div>Molar Mass: <strong>${data.molar_mass} g/mol</strong></div>
      <div>State at STP: <strong>${data.state}</strong></div>
      <div>Solubility: <strong>${data.solubility}</strong></div>
      <div>Properties: <strong>${data.properties}</strong></div>
    `;
  } else if (category === 'polyatomic_ions') {
    title = `${data.name} (${renderChemFormula(data.formula)})`;
    details = `
      <div>Charge: <strong>${data.charge > 0 ? '+' + data.charge : data.charge}</strong></div>
    `;
  } else if (category === 'reaction_types') {
    title = data.type;
    details = `
      <div>Pattern: <strong>${renderChemFormula(data.pattern)}</strong></div>
      <div>Example: <strong>${renderChemFormula(data.example)}</strong></div>
      <div style="margin-top: 6px;"><strong>Tips:</strong></div>
      <ul style="margin: 4px 0 0 16px; padding: 0; font-size:12px;">
        ${data.tips.map(t => `<li>${t}</li>`).join('')}
      </ul>
    `;
  }

  return `
    <div class="kb-card">
      <div class="kb-card-badge">${badge}</div>
      <div class="kb-card-title">${title}</div>
      <div class="kb-card-details">${details}</div>
    </div>
  `;
}

// ── Setup and Wiring ──────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {
  // Solver calc type visibility toggling
  const calcType = document.getElementById('solver-calc-type');
  if (calcType) {
    calcType.addEventListener('change', () => {
      document.querySelectorAll('.solver-fields').forEach(f => f.style.display = 'none');
      const target = document.getElementById(`fields-${calcType.value}`);
      if (target) target.style.display = 'block';
    });
  }

  // Solver calculate btn wiring
  const calcBtn = document.getElementById('solver-calculate-btn');
  if (calcBtn) {
    calcBtn.addEventListener('click', runChemistrySolve);
  }

  // KB search trigger wiring
  const kbInput = document.getElementById('kb-query-input');
  if (kbInput) {
    kbInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') runKBSearch();
    });
  }

  const kbSearchBtn = document.getElementById('kb-search-btn');
  if (kbSearchBtn) {
    kbSearchBtn.addEventListener('click', runKBSearch);
  }

  const kbCatSelect = document.getElementById('kb-category-select');
  if (kbCatSelect) {
    kbCatSelect.addEventListener('change', runKBSearch);
  }
});
