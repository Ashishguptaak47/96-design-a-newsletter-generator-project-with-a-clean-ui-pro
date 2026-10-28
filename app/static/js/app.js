let blocks = [];

document.addEventListener('DOMContentLoaded', () => {
  // Default initial block
  addBlock('article', 'Welcome to Our First Issue!', 'This is your newsletter content rendered from markdown. Feel free to edit dynamic blocks.', 'https://example.com');
  renderPreview();
});

function addBlock(type, title = '', content = '', link = '') {
  const id = Date.now() + Math.random();
  blocks.push({ id, type, title, content, link });
  renderBlockForms();
  renderPreview();
}

function removeBlock(id) {
  blocks = blocks.filter(b => b.id !== id);
  renderBlockForms();
  renderPreview();
}

function updateBlock(id, field, value) {
  const block = blocks.find(b => b.id === id);
  if (block) {
    block[field] = value;
    renderPreview();
  }
}

function renderBlockForms() {
  const container = document.getElementById('blocks-container');
  container.innerHTML = '';

  blocks.forEach((block, idx) => {
    const card = document.createElement('div');
    card.className = 'block-card';
    card.innerHTML = `
      <div class="block-header">
        <span>${idx + 1}. ${block.type.toUpperCase()} BLOCK</span>
        <button class="remove-btn" onclick="removeBlock(${block.id})"><i class="fa-solid fa-trash"></i></button>
      </div>
      <div class="form-group">
        <label>Title / Headline</label>
        <input type="text" value="${escapeAttr(block.title)}" oninput="updateBlock(${block.id}, 'title', this.value)">
      </div>
      ${block.type !== 'cta' ? `
      <div class="form-group">
        <label>Content (Markdown)</label>
        <textarea rows="3" oninput="updateBlock(${block.id}, 'content', this.value)">${block.content}</textarea>
      </div>` : ''}
      <div class="form-group">
        <label>Link URL</label>
        <input type="url" value="${escapeAttr(block.link)}" oninput="updateBlock(${block.id}, 'link', this.value)">
      </div>
    `;
    container.appendChild(card);
  });
}

function escapeAttr(str) {
  return (str || '').replace(/"/g, '&quot;');
}

function getNewsletterPayload() {
  return {
    title: document.getElementById('title').value,
    tagline: document.getElementById('tagline').value,
    footer: document.getElementById('footer').value,
    blocks: blocks
  };
}

async function renderPreview() {
  const payload = getNewsletterPayload();
  try {
    const response = await fetch('/api/preview', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    
    // Update iframe
    const iframe = document.getElementById('preview-frame');
    iframe.srcdoc = data.html;
    
    // Update Markdown
    document.getElementById('markdown-output').value = data.markdown;
  } catch (err) {
    console.error('Failed to render preview:', err);
  }
}

function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  
  if (tab === 'html') {
    document.querySelectorAll('.tab-btn')[0].classList.add('active');
    document.getElementById('html-preview-tab').classList.add('active');
  } else {
    document.querySelectorAll('.tab-btn')[1].classList.add('active');
    document.getElementById('markdown-preview-tab').classList.add('active');
  }
}

async function importRSS() {
  const url = document.getElementById('rss-url').value;
  if (!url) return alert('Please enter a valid RSS feed URL');
  
  const resultsDiv = document.getElementById('rss-results');
  resultsDiv.innerHTML = '<div style="padding:10px;color:#94a3b8;">Fetching RSS...</div>';
  
  try {
    const response = await fetch('/api/fetch-rss', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await response.json();
    resultsDiv.innerHTML = '';
    
    if (!data.articles || data.articles.length === 0) {
      resultsDiv.innerHTML = '<div style="padding:10px;color:#f43f5e;">No articles found.</div>';
      return;
    }
    
    data.articles.forEach(art => {
      const item = document.createElement('div');
      item.className = 'rss-item';
      item.innerHTML = `
        <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:260px;">${art.title}</span>
        <button class="btn-sm" onclick="addBlock('article', '${escapeAttr(art.title)}', '${escapeAttr(art.summary)}', '${escapeAttr(art.link)}')">Add</button>
      `;
      resultsDiv.appendChild(item);
    });
  } catch (e) {
    resultsDiv.innerHTML = '<div style="padding:10px;color:#f43f5e;">Failed to parse RSS feed.</div>';
  }
}

async function exportFile(format) {
  const payload = {
    format: format,
    newsletter: getNewsletterPayload()
  };
  
  const response = await fetch('/api/export', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  
  const blob = await response.blob();
  const downloadUrl = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = downloadUrl;
  a.download = `newsletter.${format === 'markdown' ? 'md' : 'html'}`;
  document.body.appendChild(a);
  a.click();
  a.remove();
}
