# -*- coding: utf-8 -*-
"""Gộp 9 trang thành web một trang + file nội dung noidung.json (sửa trực tiếp được trên Claude).
Chạy SAU build.py:  python3 build/build.py && python3 build/spa.py
Sinh:
  noidung.json          — nội dung toàn bộ 9 trang (NGUỒN CHÍNH sau khi sửa trên Claude)
  dist/index.html       — bản GitHub (đầy đủ <!doctype>)
  dist/preview.html     — bản Claude (không <!doctype>, Claude tự bọc khung)
Lưu ý: chỉ chạy lại spa.py với --reset nếu muốn GHI ĐÈ noidung.json bằng nội dung từ build.py."""
import os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index", "threads", "kol-koc", "megalive", "tiktok", "shopee", "dai-ly", "hasaki", "website"]

def fragment(name):
    s = open(os.path.join(ROOT, name + ".html"), encoding="utf-8").read()
    title = re.search(r"<title>(.*?)</title>", s).group(1)
    body = s.split("<body>\n", 1)[1].split('<script src="config.js">')[0]
    body = re.sub(r'href="index\.html"', 'href="#"', body)
    body = re.sub(r'href="(%s)\.html"' % "|".join(PAGES[1:]), r'href="#\1"', body)
    body = re.sub(r'<a href="#(muc-\d+)">', r'<a data-goto="\1">', body)
    return title, body.strip()

def make_data():
    pages, titles = {}, {}
    for n in PAGES:
        titles[n], pages[n] = fragment(n)
    return {"version": 1, "note": "", "titles": titles, "pages": pages}

APP_JS = r"""
(() => {
  const app = document.getElementById('app');
  const $ = s => document.querySelector(s);
  let DATA = null, cur = 'index', drafts = {}, editing = false, artifact = null, assets = null;

  // ── Hiển thị trang theo #hash ──
  function pageFromHash() { const h = decodeURIComponent(location.hash.slice(1)); return DATA && DATA.pages[h] ? h : 'index'; }
  function render(name, keepScroll) {
    if (editing && cur) drafts[cur] = clean(app);
    cur = name;
    app.innerHTML = drafts[name] ?? DATA.pages[name];
    document.title = (DATA.titles && DATA.titles[name]) || 'Booming Ninemila';
    if (!keepScroll) window.scrollTo(0, 0);
    initToc();
    initEmbed();
    if (editing) setEditable(true);
  }
  window.addEventListener('hashchange', () => DATA && render(pageFromHash()));

  // ── Tương tác chung (gắn một lần, ủy quyền sự kiện) ──
  document.addEventListener('click', e => {
    const mb = e.target.closest('.menu > button');
    if (mb) { e.stopPropagation(); mb.parentNode.classList.toggle('open'); return; }
    document.querySelectorAll('.menu.open').forEach(m => m.classList.remove('open'));
    const g = e.target.closest('[data-goto]');
    if (g) { e.preventDefault(); document.getElementById(g.dataset.goto)?.scrollIntoView({behavior: 'smooth'}); return; }
    const chip = e.target.closest('#matrixChips .chip');
    if (chip && !editing) {
      chip.parentNode.querySelectorAll('.chip').forEach(x => x.setAttribute('aria-pressed', x === chip));
      document.querySelectorAll('#matrix tbody tr').forEach(r => r.classList.toggle('hide', chip.dataset.g !== 'all' && r.dataset.g !== chip.dataset.g));
      return;
    }
    if (editing) {
      const slot = e.target.closest('.slot');
      if (slot && app.contains(slot)) { e.preventDefault(); if (e.target.closest('.slot-del')) removeImg(slot); else pickImage(slot); return; }
      const a = e.target.closest('a');
      if (a && app.contains(a) && !a.closest('.menu-list') && !a.closest('.pager')) e.preventDefault();
    }
  });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') document.querySelectorAll('.menu.open').forEach(m => m.classList.remove('open')); });
  let io;
  function initToc() {
    io?.disconnect();
    const links = [...app.querySelectorAll('.toc a[data-goto]')]; if (!links.length || !('IntersectionObserver' in window)) return;
    io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) links.forEach(a => a.classList.toggle('on', a.dataset.goto === en.target.id)); }), { rootMargin: '-20% 0px -70% 0px' });
    app.querySelectorAll('.content section[id]').forEach(s => io.observe(s));
  }

  // ── Nhúng trang khác (Fanpage & Instagram) ──
  // Trên GitHub: hiện trang trong khung. Trên Claude (không cho nhúng web khác): hiện thẻ giới thiệu + nút mở.
  function initEmbed() {
    app.querySelectorAll('.embed[data-src]').forEach(el => {
      const src = el.dataset.src;
      if (window.claude) {
        el.classList.add('is-card');
        el.innerHTML = '<div class="embed-card"><b>Trang lịch &amp; brief đang vận hành</b><p>Bản xem trên Claude không nhúng được trang web khác. Trên bản GitHub, trang này hiện ngay tại đây.</p><a class="btn-dark" href="' + src + '" target="_blank" rel="noopener">Mở trang lịch content ↗</a></div>';
      } else {
        el.classList.add('is-frame');
        el.innerHTML = '<iframe src="' + src + '" title="Lịch &amp; brief content fanpage Ninemila" loading="lazy"></iframe>';
      }
    });
  }

  // ── Chế độ sửa ──
  const LOCK = '.menu, .top nav, .slot, .chips, .go, .toc, .stack, .embed';
  function setEditable(on) {
    app.contentEditable = on ? 'true' : 'false';
    app.querySelectorAll(LOCK).forEach(el => el.contentEditable = on ? 'false' : 'inherit');
    app.querySelectorAll('.slot').forEach(s => {
      s.querySelector('.slot-tools')?.remove();
      if (on) s.insertAdjacentHTML('beforeend', '<div class="slot-tools"><span>Bấm để tải ảnh</span>' + (s.classList.contains('has-img') ? '<button type="button" class="slot-del">Xoá ảnh</button>' : '') + '</div>');
    });
    document.body.classList.toggle('editing', on);
  }
  function clean(root) {
    const c = root.cloneNode(true);
    c.querySelectorAll('.slot-tools').forEach(x => x.remove());
    c.querySelectorAll('[contenteditable]').forEach(x => x.removeAttribute('contenteditable'));
    c.querySelectorAll('.menu.open').forEach(x => x.classList.remove('open'));
    c.querySelectorAll('.toc a.on').forEach(x => x.classList.remove('on'));
    c.querySelectorAll('tr.hide').forEach(x => x.classList.remove('hide'));
    c.querySelectorAll('.embed').forEach(x => { x.innerHTML = ''; x.classList.remove('is-frame', 'is-card'); });
    return c.innerHTML;
  }
  const fileInput = Object.assign(document.createElement('input'), { type: 'file', accept: 'image/*', hidden: true });
  document.body.appendChild(fileInput);
  let pendingSlot = null;
  function pickImage(slot) {
    if (!assets) { status('Không tải ảnh được ở chế độ xem này.'); return; }
    pendingSlot = slot; fileInput.value = ''; fileInput.click();
  }
  fileInput.addEventListener('change', async () => {
    const f = fileInput.files[0], slot = pendingSlot; if (!f || !slot) return;
    if (f.size > 20 * 1024 * 1024) { status('Ảnh quá 20 MB, chọn ảnh nhỏ hơn.'); return; }
    status('Đang tải ảnh lên…');
    try {
      const r = await assets.upload(f);
      slot.querySelector('img')?.remove();
      const im = document.createElement('img'); im.src = r.url; im.alt = slot.getAttribute('aria-label') || ''; im.dataset.asset = r.id;
      slot.prepend(im); slot.classList.add('has-img'); setEditable(true); dirty();
      status('Đã gắn ảnh. Bấm Lưu để giữ lại.');
    } catch (e) { status('Tải ảnh không thành công (' + (e.code || 'lỗi') + '). Thử lại với ảnh khác.'); }
  });
  function removeImg(slot) { slot.querySelector('img')?.remove(); slot.classList.remove('has-img'); setEditable(true); dirty(); status('Đã xoá ảnh khỏi khung. Bấm Lưu để giữ lại.'); }

  // ── Thanh công cụ ──
  const bar = document.getElementById('editbar');
  function status(t) { bar.querySelector('.eb-status').textContent = t; }
  let changed = false;
  function dirty() { changed = true; bar.classList.add('dirty'); }
  app.addEventListener('input', () => editing && dirty());
  bar.querySelector('.eb-start').onclick = () => { editing = true; drafts = {}; changed = false; bar.classList.add('open'); bar.querySelector('#ebNote').value = DATA.note || ''; setEditable(true); status('Bấm vào chữ để sửa, bấm khung ảnh để tải ảnh. Chuyển trang bằng menu "Các kế hoạch", phần đã sửa vẫn được giữ.'); };
  bar.querySelector('.eb-cancel').onclick = () => { editing = false; drafts = {}; changed = false; bar.classList.remove('open', 'dirty'); setEditable(false); render(cur, true); };
  bar.querySelector('#ebNote').addEventListener('input', dirty);
  bar.querySelector('.eb-save').onclick = async () => {
    drafts[cur] = clean(app);
    const next = { ...DATA, pages: { ...DATA.pages, ...drafts }, note: bar.querySelector('#ebNote').value, updated: new Date().toISOString() };
    const btn = bar.querySelector('.eb-save'); btn.disabled = true; status('Đang lưu…');
    try {
      await artifact.publish({ 'noidung.json': { content: JSON.stringify(next), contentType: 'application/json' } });
      DATA = next; drafts = {}; changed = false; bar.classList.remove('dirty');
      status('Đã lưu ' + new Date().toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'}) + '. Người khác mở link sẽ thấy bản mới.');
    } catch (e) {
      const m = { conflict: 'Có người vừa lưu bản khác, trang đang tải lại bản mới nhất.', not_writer: 'Tài khoản này chỉ được xem, không lưu được.', not_granted: 'Tài khoản này chỉ được xem, không lưu được.', too_large: 'Nội dung quá lớn để lưu.', rate_limited: 'Lưu quá nhanh, đợi vài giây rồi bấm Lưu lại.' };
      status(m[e.code] || 'Chưa lưu được (' + (e.code || 'lỗi') + '). Thử bấm Lưu lại.');
    } finally { btn.disabled = false; }
  };
  window.addEventListener('beforeunload', e => { if (editing && changed) { e.preventDefault(); e.returnValue = ''; } });

  // ── Khởi động ──
  (async () => {
    try { DATA = await fetch('noidung.json', { cache: 'no-store' }).then(r => r.json()); }
    catch (e) { app.innerHTML = '<p style="padding:40px">Không tải được nội dung (noidung.json).</p>'; return; }
    render(pageFromHash());
    if (window.claude?.use) {
      artifact = await window.claude.use('artifact');
      assets = await window.claude.use('assets');
      if (artifact) bar.hidden = false;
    }
  })();
})();
"""

EDIT_CSS = """
.toc a[data-goto]{cursor:pointer}
/* ── Khung nhúng trang Fanpage ── */
.embed-sec{padding-top:40px}
.embed-bar{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:14px}
.embed-bar .label{color:var(--orange)}
.embed-bar a{font:600 13px "Be Vietnam Pro";color:var(--choco)}
.embed.is-frame iframe{display:block;width:100%;height:calc(100vh - 40px);min-height:640px;border:1px solid var(--grey);background:#fff}
.embed-card{border:1px solid var(--grey);background:var(--cream);padding:40px;display:grid;gap:12px;justify-items:start;max-width:720px}
.embed-card b{font:700 24px/1.2 "Philosopher",serif;color:var(--choco)}
.embed-card p{color:var(--muted)}
.btn-dark{display:inline-block;background:var(--choco);color:#fff;text-decoration:none;font:600 14px "Be Vietnam Pro";padding:12px 20px;border-radius:2px}
.btn-dark:hover{background:var(--orange)}
/* ── Thanh sửa nội dung (chỉ hiện trên Claude) ── */
#editbar{position:fixed;right:max(16px,env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:50;font-family:"Be Vietnam Pro",sans-serif}
#editbar .eb-start{background:var(--choco);color:#fff;border:0;border-radius:999px;padding:13px 20px;font:600 14px "Be Vietnam Pro";box-shadow:0 10px 28px rgba(45,8,0,.35);cursor:pointer}
#editbar .eb-start:hover{background:var(--orange)}
#editbar .eb-panel{display:none;width:min(360px,calc(100vw - 32px));background:#fff;border:1px solid var(--grey);box-shadow:0 18px 44px rgba(45,8,0,.28);padding:16px;border-top:4px solid var(--orange)}
#editbar.open .eb-start{display:none}
#editbar.open .eb-panel{display:grid;gap:10px}
#editbar .eb-title{font:700 17px "Philosopher",serif;color:var(--choco);display:flex;justify-content:space-between;align-items:center}
#editbar .eb-title i{font:600 10px "Josefin Sans";letter-spacing:.14em;text-transform:uppercase;font-style:normal;color:var(--orange);display:none}
#editbar.dirty .eb-title i{display:inline}
#editbar .eb-status{font-size:13px;color:var(--muted);line-height:1.45}
#editbar label{font:600 10px/1.5 "Josefin Sans";letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
#editbar textarea{width:100%;min-height:70px;border:1px solid var(--grey);padding:8px 10px;font:14px "Be Vietnam Pro";color:var(--ink);resize:vertical}
#editbar .eb-row{display:flex;gap:8px}
#editbar .eb-row button{flex:1;padding:11px;border:1px solid var(--choco);background:#fff;color:var(--choco);font:600 14px "Be Vietnam Pro";cursor:pointer;border-radius:2px}
#editbar .eb-row .eb-save{background:var(--choco);color:#fff}
#editbar .eb-row .eb-save:hover{background:var(--orange);border-color:var(--orange)}
#editbar .eb-row button:disabled{opacity:.5}
body.editing #app [contenteditable="true"]:focus,body.editing #app:focus{outline:none}
body.editing #app *:not(.slot):not(.slot *):hover{outline:1px dashed rgba(241,97,0,.55);outline-offset:2px}
body.editing #app [contenteditable="false"]:hover{outline:none}
body.editing .slot{cursor:pointer}
.slot-tools{position:absolute;top:10px;right:10px;display:flex;gap:6px;z-index:3}
.slot-tools span,.slot-tools button{font:600 11px "Be Vietnam Pro";background:var(--orange);color:#fff;border:0;padding:7px 10px;border-radius:2px}
.slot-tools button{background:#fff;color:var(--choco);cursor:pointer}
"""

def shell(css, preview):
    head = """<title>Booming Ninemila</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="robots" content="noindex, nofollow">
<meta name="color-scheme" content="light only">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Josefin+Sans:wght@400;600&family=Philosopher:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet">
<style>""" + css + EDIT_CSS + """</style>"""
    bar = """<div id="editbar" hidden>
  <button class="eb-start" type="button">✎ Sửa nội dung</button>
  <div class="eb-panel" role="dialog" aria-label="Sửa nội dung">
    <div class="eb-title">Đang sửa nội dung <i>Chưa lưu</i></div>
    <div class="eb-status"></div>
    <label for="ebNote">Ghi chú cho Claude</label>
    <textarea id="ebNote" placeholder="Ví dụ: đổi thứ tự mục, thêm bảng, chỗ nào cần Claude làm giúp…"></textarea>
    <div class="eb-row"><button class="eb-cancel" type="button">Huỷ</button><button class="eb-save" type="button">Lưu</button></div>
  </div>
</div>"""
    body = f'<div id="app"></div>\n{bar}\n<script>{APP_JS}</script>'
    if preview:
        return head + "\n" + body + "\n"
    return ('<!doctype html>\n<html lang="vi">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + "\n</head>\n<body>\n" + body + "\n</body>\n</html>\n")

if __name__ == "__main__":
    css = open(os.path.join(ROOT, "site.css"), encoding="utf-8").read()
    dist = os.path.join(ROOT, "dist"); os.makedirs(dist, exist_ok=True)
    open(os.path.join(dist, "index.html"), "w", encoding="utf-8").write(shell(css, False))
    open(os.path.join(dist, "preview.html"), "w", encoding="utf-8").write(shell(css, True))
    data_path = os.path.join(ROOT, "noidung.json")
    if "--reset" in sys.argv or not os.path.exists(data_path):
        json.dump(make_data(), open(data_path, "w", encoding="utf-8"), ensure_ascii=False)
        print("Đã ghi noidung.json từ build.py")
    else:
        print("Giữ nguyên noidung.json (dùng --reset để ghi đè)")
    print("Đã dựng dist/index.html và dist/preview.html")
