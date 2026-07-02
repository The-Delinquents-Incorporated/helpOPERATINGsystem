/**
 * HelpOS Chemistry.js
 * Chemistry tool panel: formula input, calculation routing, result display.
 */

const CHEM_VALUE_LABELS = {
  grams_to_moles:       'Grams',
  moles_to_grams:       'Moles',
  liters_to_moles:      'Liters at STP',
  moles_to_liters:      'Moles',
  moles_to_particles:   'Moles',
  particles_to_moles:   'Number of Particles',
};

const CHEM_TOOL_MAP = {
  molar_mass:          { tool: 'molar_mass',           needsValue: false },
  grams_to_moles:      { tool: 'convert_grams_moles',  needsValue: true,  direction: 'grams_to_moles'    },
  moles_to_grams:      { tool: 'convert_grams_moles',  needsValue: true,  direction: 'moles_to_grams'    },
  liters_to_moles:     { tool: 'stp_conversion',       needsValue: true,  direction: 'liters_to_moles'   },
  moles_to_liters:     { tool: 'stp_conversion',       needsValue: true,  direction: 'moles_to_liters'   },
  moles_to_particles:  { tool: 'avogadro_calculation', needsValue: true,  direction: 'moles_to_particles' },
  particles_to_moles:  { tool: 'avogadro_calculation', needsValue: true,  direction: 'particles_to_moles' },
};

function formatChemNumber(val) {
  if (typeof val !== 'number') return String(val);
  if (Math.abs(val) >= 1e15 || (Math.abs(val) < 1e-3 && val !== 0)) {
    return val.toExponential(4);
  }
  return parseFloat(val.toPrecision(6)).toString();
}

function renderChemResult(data) {
  const area = document.getElementById('chem-result-area');
  const err  = document.getElementById('chem-error');
  err.style.display = 'none';

  if (!data || data.mode === 'error') {
    area.innerHTML = `<p style="color:var(--accent-red); font-size:13px;">⚠ ${data?.detail || 'Calculation failed.'}</p>`;
    return;
  }

  const result = data.result || data;
  const value  = result.result ?? result.molar_mass ?? '—';
  const unit   = result.unit || '';
  const displayVal = typeof value === 'number' ? formatChemNumber(value) : String(value);

  // Build meta rows from result object
  const metaSkip = ['result', 'molar_mass', 'unit', 'is_mock'];
  const metaItems = Object.entries(result)
    .filter(([k]) => !metaSkip.includes(k))
    .map(([k, v]) => `
      <div class="result-meta-item">
        ${k.replace(/_/g, ' ')}: <strong>${typeof v === 'number' ? formatChemNumber(v) : v}</strong>
      </div>`)
    .join('');

  area.innerHTML = `
    <div class="result-card">
      <div class="result-label">Result</div>
      <div class="result-value">${displayVal}</div>
      <div class="result-unit">${unit}</div>
      ${metaItems ? `<div class="result-meta">${metaItems}</div>` : ''}
    </div>`;
}

async function runChemCalculation() {
  const formula  = document.getElementById('chem-formula').value.trim();
  const calcType = document.getElementById('chem-calc-type').value;
  const valueEl  = document.getElementById('chem-value');
  const errEl    = document.getElementById('chem-error');
  const btn      = document.getElementById('chem-calculate-btn');
  const area     = document.getElementById('chem-result-area');

  errEl.style.display = 'none';

  const mapping = CHEM_TOOL_MAP[calcType];
  if (!mapping) return;

  // Validate
  if (!formula) {
    errEl.textContent = 'Please enter a chemical formula.';
    errEl.style.display = 'block';
    return;
  }

  if (mapping.needsValue) {
    const val = parseFloat(valueEl.value);
    if (isNaN(val) || val < 0) {
      errEl.textContent = 'Please enter a valid positive value.';
      errEl.style.display = 'block';
      return;
    }
  }

  // Build messages for coordinator
  let userMsg = '';
  if (mapping.tool === 'molar_mass') {
    userMsg = `Calculate the molar mass of ${formula}.`;
  } else if (mapping.direction) {
    userMsg = `${calcType.replace(/_/g, ' ')} for ${formula} with value ${valueEl.value}.`;
  }

  btn.disabled = true;
  btn.textContent = 'Calculating…';
  area.innerHTML = '<div style="color:var(--text-muted); font-size:13px;">Computing…</div>';

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [{ role: 'user', content: userMsg }],
        stream: false
      })
    });

    const data = await res.json();
    renderChemResult(data);
  } catch (err) {
    document.getElementById('chem-result-area').innerHTML =
      `<p style="color:var(--accent-red);">⚠ Network error: ${err.message}</p>`;
  } finally {
    btn.disabled = false;
    btn.innerHTML = `
      <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 11h.01M12 11h.01M15 11h.01M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"/>
      </svg>
      Calculate`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const calcTypeEl  = document.getElementById('chem-calc-type');
  const valueGroup  = document.getElementById('chem-value-group');
  const valueLabel  = document.getElementById('chem-value-label');
  const formulaEl   = document.getElementById('chem-formula');
  const displayEl   = document.getElementById('chem-formula-display');
  const calcBtn     = document.getElementById('chem-calculate-btn');

  // Show/hide value field based on calc type
  function updateValueVisibility() {
    const type = calcTypeEl.value;
    const mapping = CHEM_TOOL_MAP[type];
    if (mapping?.needsValue) {
      valueGroup.style.display = 'block';
      valueLabel.textContent = CHEM_VALUE_LABELS[type] || 'Value';
    } else {
      valueGroup.style.display = 'none';
    }
  }

  calcTypeEl.addEventListener('change', updateValueVisibility);
  updateValueVisibility();

  // Live formula display
  formulaEl.addEventListener('input', () => {
    displayEl.textContent = formulaEl.value || '—';
  });

  // Calculate button
  calcBtn.addEventListener('click', runChemCalculation);

  // Enter key on formula input
  formulaEl.addEventListener('keydown', e => {
    if (e.key === 'Enter') runChemCalculation();
  });

  // Math solver suggestion chips
  document.querySelectorAll('.suggestion-chip[data-expr]').forEach(chip => {
    chip.addEventListener('click', () => {
      const exprEl = document.getElementById('math-expression');
      if (exprEl) {
        exprEl.value = chip.dataset.expr;
        exprEl.focus();
      }
    });
  });

  // Math solve button
  const mathSolveBtn = document.getElementById('math-solve-btn');
  const mathExprEl   = document.getElementById('math-expression');
  const mathErrEl    = document.getElementById('math-error');
  const mathResArea  = document.getElementById('math-result-area');

  async function runMathSolve() {
    const expr = mathExprEl?.value?.trim();
    if (!expr) return;

    mathErrEl.style.display = 'none';
    mathSolveBtn.disabled   = true;
    mathSolveBtn.textContent = 'Solving…';
    mathResArea.innerHTML    = '<div style="color:var(--text-muted); font-size:13px;">Computing…</div>';

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [{ role: 'user', content: `Solve the math expression: ${expr}` }],
          stream: false
        })
      });

      const data = await res.json();

      if (data.mode === 'deterministic' && data.result) {
        const val = data.result.result ?? '—';
        const displayVal = typeof val === 'number' ? formatChemNumber(val) : String(val);
        mathResArea.innerHTML = `
          <div class="result-card">
            <div class="result-label">Result</div>
            <div class="result-value">${displayVal}</div>
            ${data.result.is_mock ? '<div class="result-unit" style="color:var(--accent-amber);">⚠ Approximate (full solver in Phase 2)</div>' : ''}
          </div>`;
      } else if (data.mode === 'reasoning') {
        mathResArea.innerHTML = `<div class="message-bubble" style="margin-top:12px;">${data.content}</div>`;
      } else {
        mathResArea.innerHTML = `<p style="color:var(--accent-red);">⚠ Unexpected response.</p>`;
      }
    } catch (err) {
      mathResArea.innerHTML = `<p style="color:var(--accent-red);">⚠ Error: ${err.message}</p>`;
    } finally {
      mathSolveBtn.disabled    = false;
      mathSolveBtn.textContent = 'Solve';
    }
  }

  if (mathSolveBtn) mathSolveBtn.addEventListener('click', runMathSolve);
  if (mathExprEl)   mathExprEl.addEventListener('keydown', e => {
    if (e.key === 'Enter') runMathSolve();
  });
});
