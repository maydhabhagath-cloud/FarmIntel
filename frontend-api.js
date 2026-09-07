/* FarmIntel frontend/API bridge. Loaded by the build step so the existing UI stays intact. */
(() => {
  const API_BASE = (window.FARMINTEL_API_BASE || '/api').replace(/\/$/, '');
  const $ = (id) => document.getElementById(id);
  const toast = (msg) => window.showToast ? window.showToast(msg) : console.log(msg);

  async function api(path, options = {}) {
    const response = await fetch(API_BASE + path, {
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      ...options
    });
    if (!response.ok) throw new Error(`API ${response.status}`);
    return response.json();
  }

  function addConnectionBadge(ok, text) {
    const header = document.querySelector('.header-actions');
    if (!header || document.getElementById('apiStatus')) return;
    const badge = document.createElement('span');
    badge.id = 'apiStatus';
    badge.className = 'pill';
    badge.textContent = text;
    badge.title = 'FarmIntel backend connection status';
    header.prepend(badge);
  }

  async function checkBackend() {
    try {
      await api('/health');
      addConnectionBadge(true, 'API Online');
      return true;
    } catch (error) {
      addConnectionBadge(false, 'API Offline');
      return false;
    }
  }

  async function getCropAdvice(crop, soil = 'unknown', season = 'unknown', location = 'unknown') {
    return api('/crop-advice', {
      method: 'POST',
      body: JSON.stringify({ crop, soil, season, location })
    });
  }

  function addAssistant() {
    if ($('farmIntelAssistant')) return;
    const box = document.createElement('div');
    box.id = 'farmIntelAssistant';
    box.style.cssText = 'position:fixed;right:20px;bottom:20px;width:min(360px,calc(100vw - 40px));background:#fff;border:1px solid #e6efe6;border-radius:12px;box-shadow:0 12px 30px rgba(17,59,37,.16);padding:14px;z-index:70;display:none';
    box.innerHTML = `<div style="font-weight:700;color:#1b6b3a">FarmIntel Assistant</div><div id="fiChatLog" style="max-height:220px;overflow:auto;margin:10px 0;font-size:13px"><div class="small-muted">Ask about crops, pests, markets or selling.</div></div><div style="display:flex;gap:8px"><input id="fiChatInput" style="flex:1;padding:8px;border:1px solid #e6efe6;border-radius:8px" placeholder="Ask a farming question"><button id="fiChatSend" class="btn">Send</button></div>`;
    document.body.appendChild(box);

    const log = $('fiChatLog');
    const send = async () => {
      const input = $('fiChatInput');
      const message = input.value.trim();
      if (!message) return;
      log.insertAdjacentHTML('beforeend', `<div style="margin:7px 0"><strong>You:</strong> ${message.replace(/[<>]/g,'')}</div>`);
      input.value = '';
      try {
        const data = await api('/chat', { method: 'POST', body: JSON.stringify({ message }) });
        log.insertAdjacentHTML('beforeend', `<div style="margin:7px 0"><strong>FarmIntel:</strong> ${String(data.reply).replace(/[<>]/g,'')}</div>`);
        log.scrollTop = log.scrollHeight;
      } catch (error) {
        log.insertAdjacentHTML('beforeend', '<div style="margin:7px 0">Backend unavailable. Check the API deployment.</div>');
      }
    };
    $('fiChatSend').addEventListener('click', send);
    $('fiChatInput').addEventListener('keydown', (e) => { if (e.key === 'Enter') send(); });

    const toggle = document.createElement('button');
    toggle.id = 'fiAssistantToggle';
    toggle.className = 'btn';
    toggle.textContent = 'Ask FarmIntel';
    toggle.style.cssText = 'position:fixed;right:20px;bottom:20px;z-index:71;border-radius:999px';
    toggle.addEventListener('click', () => {
      const open = box.style.display === 'block';
      box.style.display = open ? 'none' : 'block';
      toggle.textContent = open ? 'Ask FarmIntel' : 'Close Assistant';
      if (!open) $('fiChatInput').focus();
    });
    document.body.appendChild(toggle);
  }

  async function wireLotAdvice() {
    const form = $('lotForm');
    if (!form || form.dataset.apiWired) return;
    form.dataset.apiWired = '1';
    form.addEventListener('submit', async () => {
      const crop = $('lotCrop')?.value;
      if (!crop) return;
      try {
        const data = await getCropAdvice(crop, 'unknown', 'unknown', $('lotLocation')?.value || 'unknown');
        setTimeout(() => toast(`Crop advice: ${data.advice}`), 350);
      } catch (_) {
        setTimeout(() => toast('Lot saved. Crop advice service is currently unavailable.'), 350);
      }
    });
  }

  window.FarmIntelAPI = { api, checkBackend, getCropAdvice };
  window.addEventListener('DOMContentLoaded', async () => {
    addAssistant();
    wireLotAdvice();
    await checkBackend();
  });
})();
