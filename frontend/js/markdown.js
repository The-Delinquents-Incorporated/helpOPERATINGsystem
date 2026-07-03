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
    for (const line of lines) {
      if (/^#{1,3}\s+/.test(line)) {
        const level = line.match(/^#+/)[0].length;
        html += `<h${level}>${renderInlineMarkdown(line.replace(/^#{1,3}\s+/, ''))}</h${level}>`;
      } else if (/^>\s?/.test(line)) {
        html += `<blockquote>${renderInlineMarkdown(line.replace(/^>\s?/, ''))}</blockquote>`;
      } else if (/^[-*]\s+/.test(line)) {
        if (!inList) { html += '<ul>'; inList = true; }
        html += `<li>${renderInlineMarkdown(line.replace(/^[-*]\s+/, ''))}</li>`;
      } else {
        if (inList) { html += '</ul>'; inList = false; }
        if (line.trim()) html += `<p>${renderInlineMarkdown(line)}</p>`;
      }
    }
    if (inList) html += '</ul>';
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
