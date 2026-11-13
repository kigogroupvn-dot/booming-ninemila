// Booming Ninemila · tương tác chung
(() => {
  // Menu "Các kế hoạch"
  document.querySelectorAll('.menu > button').forEach(b => {
    b.addEventListener('click', e => { e.stopPropagation(); const m = b.parentNode; m.classList.toggle('open'); b.setAttribute('aria-expanded', m.classList.contains('open')); });
  });
  document.addEventListener('click', () => document.querySelectorAll('.menu.open').forEach(m => m.classList.remove('open')));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') document.querySelectorAll('.menu.open').forEach(m => m.classList.remove('open')); });

  // Lọc ma trận IMC theo nhóm
  const chips = document.querySelector('#matrixChips');
  if (chips) chips.addEventListener('click', e => {
    const c = e.target.closest('.chip'); if (!c) return;
    chips.querySelectorAll('.chip').forEach(x => x.setAttribute('aria-pressed', x === c));
    const g = c.dataset.g;
    document.querySelectorAll('#matrix tbody tr').forEach(r => r.classList.toggle('hide', g !== 'all' && r.dataset.g !== g));
  });

  // Mục lục trang con: đánh dấu mục đang xem
  const links = [...document.querySelectorAll('.toc a')];
  if (links.length && 'IntersectionObserver' in window) {
    const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (en.isIntersecting) { links.forEach(a => a.classList.remove('on')); map.get(en.target.id)?.classList.add('on'); }
    }), { rootMargin: '-20% 0px -70% 0px' });
    document.querySelectorAll('.content section[id]').forEach(s => io.observe(s));
  }
})();

// Ảnh demo: đọc tab "Ảnh IMC" trong Google Sheet (cột Mã khung + Link ảnh), gắn vào khung có data-slot trùng mã.
(async () => {
  const url = (window.IMC_CONFIG || {}).sheetUrl || '';
  const id = (url.match(/\/d\/([\w-]{20,})/) || [])[1];
  if (!id || !window.fetch) return;
  const parseCSV = t => { const rows = []; let row = [], f = '', q = false;
    for (let i = 0; i < t.length; i++) { const c = t[i];
      if (q) { if (c === '"') { if (t[i+1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
      else if (c === '"') q = true; else if (c === ',') { row.push(f); f = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && t[i+1] === '\n') i++; row.push(f); rows.push(row); row = []; f = ''; }
      else f += c; }
    if (f !== '' || row.length) { row.push(f); rows.push(row); } return rows; };
  const img = u => { u = String(u || '').trim(); if (!/^https?:\/\//i.test(u)) return '';
    const m = u.match(/\/d\/([\w-]{20,})/) || u.match(/[?&]id=([\w-]{20,})/); return m ? `https://lh3.googleusercontent.com/d/${m[1]}=w1600` : u; };
  try {
    const r = await fetch(`https://docs.google.com/spreadsheets/d/${id}/gviz/tq?tqx=out:csv&headers=1&sheet=${encodeURIComponent('Ảnh IMC')}`, { cache: 'no-store' });
    if (!r.ok) return;
    const rows = parseCSV(await r.text()); const H = (rows[0] || []).map(h => h.toLowerCase());
    const ci = H.findIndex(h => h.startsWith('mã')), li = H.findIndex(h => h.startsWith('link'));
    if (ci < 0 || li < 0) return;
    const map = {}; rows.slice(1).forEach(x => { const k = (x[ci] || '').trim(), v = img(x[li]); if (k && v) map[k] = v; });
    if (map['nen-bia']) document.documentElement.style.setProperty('--nen', `url("${map['nen-bia'].replace(/"/g, '')}")`);
    document.querySelectorAll('[data-slot]').forEach(el => {
      const src = map[el.dataset.slot]; if (!src) return;
      const im = new Image(); im.alt = el.getAttribute('aria-label') || ''; im.loading = 'lazy';
      im.onload = () => el.classList.add('has-img'); im.src = src; el.prepend(im);
    });
  } catch (e) { /* không tải được Sheet: giữ khung mẫu */ }
})();
