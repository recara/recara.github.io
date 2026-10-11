(() => {
  'use strict';
  const cases = [...document.querySelectorAll('[data-lab]')];
  if (!cases.length) return;
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const active = new Map();
  const words = {
    ru: {play:'Запустить ↗', replay:'Повторить ↗', stop:'Остановить', running:'Иллюстрация запущена.', done:'Иллюстрация завершена.', stopped:'Иллюстрация остановлена.'},
    en: {play:'Play ↗', replay:'Replay ↗', stop:'Stop', running:'Illustration started.', done:'Illustration complete.', stopped:'Illustration stopped.'}
  };
  const text = () => words[document.documentElement.lang === 'en' ? 'en' : 'ru'];
  function refresh(item) {
    const button = item.querySelector('.lab-play');
    const key = active.has(item) ? 'stop' : item.dataset.labPlayed ? 'replay' : 'play';
    button.textContent = text()[key];
    button.setAttribute('aria-label', `${item.querySelector('h4').textContent}: ${text()[key]}`);
  }
  function end(item, complete) {
    clearTimeout(active.get(item));
    active.delete(item);
    if (complete) {item.classList.remove('lab-running', 'lab-paused');item.classList.add('lab-complete');}
    else item.classList.add('lab-paused');
    item.querySelector('.lab-status').textContent = text()[complete ? 'done' : 'stopped'];
    refresh(item);
  }
  cases.forEach(item => {
    item.classList.add('lab-ready');
    refresh(item);
    item.querySelector('.lab-play').addEventListener('click', () => {
      if (active.has(item)) {end(item, false); return;}
      item.dataset.labPlayed = 'true';
      item.classList.remove('lab-running','lab-paused','lab-complete');
      if (motion.matches) {end(item, true); return;}
      void item.getBoundingClientRect();
      item.classList.add('lab-running');
      item.querySelector('.lab-status').textContent = text().running;
      active.set(item, setTimeout(() => end(item, true), 4300));
      refresh(item);
    });
  });
  new MutationObserver(() => cases.forEach(refresh)).observe(document.documentElement, {attributes:true, attributeFilter:['lang']});
  document.addEventListener('visibilitychange', () => {if (document.hidden) [...active.keys()].forEach(item => end(item, false));});
  motion.addEventListener('change', () => {if (motion.matches) [...active.keys()].forEach(item => end(item, true));});
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting && active.has(entry.target)) end(entry.target, false);
    }));
    cases.forEach(item => observer.observe(item));
  }
})();
