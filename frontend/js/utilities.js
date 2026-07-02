/**
 * HelpOS Utilities.js
 * All client-side utility tools — no API calls.
 * JSON formatter, Base64, Regex tester, Unix Timestamp.
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── Tab switching ─────────────────────────────────────

  const tabBtns  = document.querySelectorAll('#utils-tabs .tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.tab;

      tabBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      tabPanes.forEach(p => {
        p.classList.remove('active');
        p.hidden = true;
      });

      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');
      const pane = document.getElementById(`tab-${target}`);
      if (pane) {
        pane.classList.add('active');
        pane.hidden = false;
      }
    });
  });

  // ── JSON Formatter ────────────────────────────────────

  const jsonInput    = document.getElementById('json-input');
  const jsonOutput   = document.getElementById('json-output');
  const jsonError    = document.getElementById('json-error');
  const jsonFormatBtn = document.getElementById('json-format-btn');
  const jsonMinifyBtn = document.getElementById('json-minify-btn');
  const jsonCopyBtn   = document.getElementById('json-copy-btn');

  function parseJsonSafe(str) {
    try {
      return { ok: true, data: JSON.parse(str) };
    } catch (e) {
      return { ok: false, err: e.message };
    }
  }

  function showJsonResult(text, isError = false) {
    jsonOutput.textContent = text;
    jsonError.style.display = isError ? 'block' : 'none';
    if (isError) {
      jsonError.textContent = text;
      jsonOutput.textContent = '';
    }
  }

  if (jsonFormatBtn) {
    jsonFormatBtn.addEventListener('click', () => {
      const res = parseJsonSafe(jsonInput.value);
      if (res.ok) {
        showJsonResult(JSON.stringify(res.data, null, 2));
      } else {
        showJsonResult(`JSON Error: ${res.err}`, true);
      }
    });
  }

  if (jsonMinifyBtn) {
    jsonMinifyBtn.addEventListener('click', () => {
      const res = parseJsonSafe(jsonInput.value);
      if (res.ok) {
        showJsonResult(JSON.stringify(res.data));
      } else {
        showJsonResult(`JSON Error: ${res.err}`, true);
      }
    });
  }

  if (jsonCopyBtn) {
    jsonCopyBtn.addEventListener('click', async () => {
      const text = jsonOutput.textContent;
      if (!text) return;
      try {
        await navigator.clipboard.writeText(text);
        jsonCopyBtn.textContent = 'Copied!';
        setTimeout(() => { jsonCopyBtn.textContent = 'Copy'; }, 1500);
      } catch {
        jsonCopyBtn.textContent = 'Failed';
      }
    });
  }

  // Live format on input (debounced)
  let jsonDebounce;
  if (jsonInput) {
    jsonInput.addEventListener('input', () => {
      clearTimeout(jsonDebounce);
      jsonDebounce = setTimeout(() => {
        if (!jsonInput.value.trim()) { jsonOutput.textContent = ''; return; }
        const res = parseJsonSafe(jsonInput.value);
        if (res.ok) {
          showJsonResult(JSON.stringify(res.data, null, 2));
        }
        // Don't show error on live input to avoid annoyance
      }, 400);
    });
  }

  // ── Base64 ────────────────────────────────────────────

  const b64Input     = document.getElementById('b64-input');
  const b64Output    = document.getElementById('b64-output');
  const b64Error     = document.getElementById('b64-error');
  const b64EncodeBtn = document.getElementById('b64-encode-btn');
  const b64DecodeBtn = document.getElementById('b64-decode-btn');

  if (b64EncodeBtn) {
    b64EncodeBtn.addEventListener('click', () => {
      b64Error.style.display = 'none';
      try {
        b64Output.textContent = btoa(unescape(encodeURIComponent(b64Input.value)));
      } catch (e) {
        b64Error.textContent = `Encode error: ${e.message}`;
        b64Error.style.display = 'block';
      }
    });
  }

  if (b64DecodeBtn) {
    b64DecodeBtn.addEventListener('click', () => {
      b64Error.style.display = 'none';
      try {
        b64Output.textContent = decodeURIComponent(escape(atob(b64Input.value.trim())));
      } catch (e) {
        b64Error.textContent = `Decode error: Invalid Base64 string.`;
        b64Error.style.display = 'block';
      }
    });
  }

  // ── Regex Tester ──────────────────────────────────────

  const regexPattern  = document.getElementById('regex-pattern');
  const regexFlags    = document.getElementById('regex-flags');
  const regexTestStr  = document.getElementById('regex-test-str');
  const regexResultArea = document.getElementById('regex-result-area');

  function runRegex() {
    if (!regexPattern || !regexResultArea) return;
    const pattern = regexPattern.value;
    const flags   = (regexFlags?.value || '').replace(/[^gimsuy]/g, '');
    const testStr = regexTestStr?.value || '';

    if (!pattern) {
      regexResultArea.innerHTML = '';
      return;
    }

    try {
      const rx      = new RegExp(pattern, flags);
      const matches = [...testStr.matchAll(new RegExp(pattern, flags.includes('g') ? flags : flags + 'g'))];

      if (matches.length === 0) {
        regexResultArea.innerHTML = `
          <div class="result-card" style="border-color:var(--accent-amber);">
            <div class="result-label">No matches</div>
            <div style="color:var(--text-muted); font-size:13px;">The pattern did not match any text.</div>
          </div>`;
        return;
      }

      const matchList = matches.map((m, i) => `
        <div style="margin-bottom:6px; font-size:12px;">
          <span style="color:var(--accent-cyan); font-family:var(--font-mono);">[${i}]</span>
          <span style="font-family:var(--font-mono); color:var(--text-primary); margin-left:8px;">${escapeForDisplay(m[0])}</span>
          <span style="color:var(--text-muted); margin-left:8px;">@ index ${m.index}</span>
        </div>`).join('');

      regexResultArea.innerHTML = `
        <div class="result-card">
          <div class="result-label">${matches.length} match${matches.length !== 1 ? 'es' : ''}</div>
          <div style="margin-top:8px;">${matchList}</div>
        </div>`;
    } catch (e) {
      regexResultArea.innerHTML = `
        <div class="result-card" style="border-color:var(--accent-red);">
          <div class="result-label" style="color:var(--accent-red);">Invalid regex</div>
          <div style="color:var(--text-muted); font-size:13px;">${e.message}</div>
        </div>`;
    }
  }

  function escapeForDisplay(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '↵')
      .replace(/\t/g, '→');
  }

  let regexDebounce;
  [regexPattern, regexFlags, regexTestStr].forEach(el => {
    el?.addEventListener('input', () => {
      clearTimeout(regexDebounce);
      regexDebounce = setTimeout(runRegex, 200);
    });
  });

  // ── Unix Timestamp ────────────────────────────────────

  const tsInput      = document.getElementById('ts-input');
  const tsNowBtn     = document.getElementById('ts-now-btn');
  const tsConvertBtn = document.getElementById('ts-convert-btn');
  const tsResultArea = document.getElementById('ts-result-area');

  function convertTimestamp(ts) {
    const num = parseInt(ts, 10);
    if (isNaN(num)) {
      tsResultArea.innerHTML = `<p style="color:var(--accent-red); font-size:13px;">Invalid timestamp.</p>`;
      return;
    }

    // Detect if ms or seconds
    const isMs  = num > 1e12;
    const ms    = isMs ? num : num * 1000;
    const date  = new Date(ms);

    const localStr = date.toLocaleString(undefined, { dateStyle: 'full', timeStyle: 'long' });
    const isoStr   = date.toISOString();
    const utcStr   = date.toUTCString();
    const unixSec  = Math.floor(ms / 1000);
    const unixMs   = ms;

    tsResultArea.innerHTML = `
      <div class="result-card">
        <div class="result-label">Timestamp Conversion</div>
        <div style="margin-top:10px; display:flex; flex-direction:column; gap:8px;">
          ${row('Local Time',    localStr)}
          ${row('ISO 8601',      isoStr)}
          ${row('UTC',           utcStr)}
          ${row('Unix (seconds)', unixSec.toLocaleString())}
          ${row('Unix (ms)',     unixMs.toLocaleString())}
        </div>
      </div>`;
  }

  function row(label, val) {
    return `
      <div style="font-size:12px;">
        <span style="color:var(--text-muted); min-width:130px; display:inline-block;">${label}</span>
        <span style="font-family:var(--font-mono); color:var(--text-primary);">${val}</span>
      </div>`;
  }

  if (tsNowBtn) {
    tsNowBtn.addEventListener('click', () => {
      const now = Math.floor(Date.now() / 1000);
      tsInput.value = String(now);
      convertTimestamp(now);
    });
  }

  if (tsConvertBtn) {
    tsConvertBtn.addEventListener('click', () => convertTimestamp(tsInput.value));
  }

  if (tsInput) {
    tsInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') convertTimestamp(tsInput.value);
    });
  }

});
