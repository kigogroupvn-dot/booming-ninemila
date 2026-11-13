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
