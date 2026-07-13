/**
 * HelpOS Markdown.js
 * Shared markdown renderer for chat, docs, and study previews.
 */

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

/** Render LaTeX-style chemistry notation as compact Unicode text. */
function renderChemFormula(text) {
  const subscripts = { 0: '₀', 1: '₁', 2: '₂', 3: '₃', 4: '₄', 5: '₅', 6: '₆', 7: '₇', 8: '₈', 9: '₉' };
  const superscripts = {
    0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
    5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹',
    '+': '⁺', '-': '⁻'
  };
  const convert = (value, table) => [...value].map(char => table[char] || char).join('');

  const formatted = String(text ?? '')
    .replace(/\s+/g, '')
    .replace(/\^\{([^}]+)\}/g, (_, value) => convert(value, superscripts))
    .replace(/\^(\d*[+-])/g, (_, value) => convert(value, superscripts))
    .replace(/_\{(\d+)\}/g, (_, value) => convert(value, subscripts))
    .replace(/_(\d+)/g, (_, value) => convert(value, subscripts));

  return escapeHtml(formatted);
}

function renderInlineMarkdown(text) {
  const underlineBlocks = [];
  let processed = String(text || '').replace(/<u>([\s\S]*?)<\/u>/gi, (_, inner) => {
    const token = `@@UNDERLINE_${underlineBlocks.length}@@`;
    underlineBlocks.push(`<u>${escapeHtml(inner)}</u>`);
    return token;
  });

  processed = escapeHtml(processed);

  underlineBlocks.forEach((html, index) => {
    processed = processed.replace(`@@UNDERLINE_${index}@@`, html);
  });

  return processed
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<![A-Za-z0-9])_([^_\n]+?)_(?![A-Za-z0-9])/g, '<em>$1</em>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>')
    .replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
    .replace(/([A-Za-z\)])(\d+)/g, (_, prefix, digits) => `${prefix}<sub>${digits}</sub>`)
    .replace(/\^(-?\d+)/g, (_, digits) => `<sup>${digits}</sup>`);
}

function renderMarkdown(text) {
  if (typeof marked !== 'undefined') {
    const html = marked.parse(text, { breaks: true });
    return html
      .replace(/<u>([\s\S]*?)<\/u>/gi, '<u>$1</u>')
      .replace(/(?<![A-Za-z0-9])_([^_\n<]+?)_(?![A-Za-z0-9])/g, '<em>$1</em>');
  }

  const chunks = String(text || '').split(/```([\s\S]*?)```/g);
  return chunks.map((chunk, index) => {
    if (index % 2 === 1) {
      const code = chunk.replace(/^\w+\n/, '');
      return `<div class="code-block-wrap"><button class="copy-code-btn" type="button">Copy</button><pre><code>${escapeHtml(code.trim())}</code></pre></div>`;
    }

    const lines = chunk.split(/\n/);
    let html = '';
    let inList = false;
    let listTag = 'ul';
    for (const line of lines) {
      if (/^#{1,3}\s+/.test(line)) {
        if (inList) { html += `</${listTag}>`; inList = false; }
        const level = line.match(/^#+/)[0].length;
        html += `<h${level}>${renderInlineMarkdown(line.replace(/^#{1,3}\s+/, ''))}</h${level}>`;
      } else if (/^>\s?/.test(line)) {
        if (inList) { html += `</${listTag}>`; inList = false; }
        html += `<blockquote>${renderInlineMarkdown(line.replace(/^>\s?/, ''))}</blockquote>`;
      } else if (/^[-*]\s+/.test(line)) {
        if (!inList || listTag !== 'ul') {
          if (inList) html += `</${listTag}>`;
          html += '<ul>';
          inList = true;
          listTag = 'ul';
        }
        html += `<li>${renderInlineMarkdown(line.replace(/^[-*]\s+/, ''))}</li>`;
      } else if (/^\d+\.\s+/.test(line)) {
        if (!inList || listTag !== 'ol') {
          if (inList) html += `</${listTag}>`;
          html += '<ol>';
          inList = true;
          listTag = 'ol';
        }
        html += `<li>${renderInlineMarkdown(line.replace(/^\d+\.\s+/, ''))}</li>`;
      } else {
        if (inList) { html += `</${listTag}>`; inList = false; }
        if (line.trim()) html += `<p>${renderInlineMarkdown(line)}</p>`;
      }
    }
    if (inList) html += `</${listTag}>`;
    return html;
  }).join('');
}

function wireCopyCodeButtons(root) {
  (root || document).querySelectorAll('.copy-code-btn').forEach(btn => {
    if (btn.dataset.wired === 'true') return;
    btn.dataset.wired = 'true';
    btn.addEventListener('click', () => {
      const code = btn.parentElement.querySelector('code')?.textContent || '';
      navigator.clipboard?.writeText(code);
      btn.textContent = 'Copied';
      setTimeout(() => { btn.textContent = 'Copy'; }, 1200);
    });
  });
}
