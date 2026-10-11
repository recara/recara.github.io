(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const runs = new Map();
  let language = 'ru';
  const copy = {
    ru: {play:'Запустить ↗', stop:'Остановить', replay:'Повторить ↗', group:'Собрать по смыслу', scatter:'Перемешать снова', done:'Иллюстрация завершена.', stopped:'Иллюстрация остановлена.', running:'Иллюстрация запущена.'},
    en: {play:'Play ↗', stop:'Stop', replay:'Replay ↗', group:'Group by meaning', scatter:'Scatter again', done:'Illustration complete.', stopped:'Illustration stopped.', running:'Illustration started.'}
  };
  const label = (button, key) => {button.textContent = copy[language][key];};
  function updateControls() {
    document.querySelectorAll('[data-play]').forEach(button => {
      const figure = button.closest('[data-demo]');
      const key = runs.has(figure) ? 'stop' : figure.dataset.played === 'true' ? 'replay' : 'play';
      label(button, key);
      button.setAttribute('aria-label', `${figure.dataset.demo}: ${copy[language][key]}`);
    });
    const clusterButton = document.querySelector('.cluster-button');
    if (clusterButton) label(clusterButton, clusterButton.getAttribute('aria-pressed') === 'true' ? 'scatter' : 'group');
  }
  function setLang(next) {
    if (!['ru', 'en'].includes(next)) return;
    language = next;
    document.documentElement.lang = next;
    document.querySelectorAll('[data-set-lang]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.setLang === next)));
    updateControls();
    try { localStorage.setItem('lang', next); } catch (_) { /* Storage can be disabled. */ }
  }
  let saved;
  try { saved = localStorage.getItem('lang'); } catch (_) { /* Use the page default. */ }
  setLang(saved === 'en' ? 'en' : 'ru');
  document.querySelectorAll('[data-set-lang]').forEach(button => button.addEventListener('click', () => setLang(button.dataset.setLang)));
  document.querySelector('.cluster-button')?.addEventListener('click', event => {
    const button = event.currentTarget;
    const enabled = button.getAttribute('aria-pressed') !== 'true';
    button.setAttribute('aria-pressed', String(enabled));
    button.closest('.cluster-paper').classList.toggle('is-clustered', enabled);
    updateControls();
  });
  function setCounts(figure, value) { figure.querySelectorAll('[data-count]').forEach(node => {node.textContent = String(value);}); }
  function finish(figure) {
    const timers = runs.get(figure);
    if (timers) timers.forEach(clearTimeout);
    runs.delete(figure);
    figure.classList.remove('is-playing', 'is-paused');
    figure.classList.add('is-complete');
    setCounts(figure, 1);
    figure.querySelector('.demo-status').textContent = copy[language].done;
    updateControls();
  }
  function stop(figure) {
    const timers = runs.get(figure);
    if (timers) timers.forEach(clearTimeout);
    runs.delete(figure);
    figure.classList.add('is-paused');
    figure.querySelector('.demo-status').textContent = copy[language].stopped;
    updateControls();
  }
  document.querySelectorAll('[data-play]').forEach(button => {
    button.addEventListener('click', () => {
      const figure = button.closest('[data-demo]');
      if (runs.has(figure)) { stop(figure); return; }
      figure.dataset.played = 'true';
      figure.classList.remove('is-playing', 'is-complete', 'is-paused');
      setCounts(figure, 0);
      if (reducedMotion.matches) { finish(figure); return; }
      // Flush the previous sequence before restarting the same finite animation.
      void figure.getBoundingClientRect();
      figure.classList.add('is-playing');
      figure.querySelector('.demo-status').textContent = copy[language].running;
      const timers = [setTimeout(() => setCounts(figure, 1), figure.dataset.demo === 'trafficvision' ? 4900 : 2850), setTimeout(() => finish(figure), 5500)];
      runs.set(figure, timers);
      updateControls();
    });
  });
  const stopActive = () => { [...runs.keys()].forEach(stop); };
  document.addEventListener('visibilitychange', () => { if (document.hidden) stopActive(); });
  reducedMotion.addEventListener('change', () => { if (reducedMotion.matches) [...runs.keys()].forEach(finish); });
  if ('IntersectionObserver' in window) {
    const sequenceObserver = new IntersectionObserver(entries => { entries.forEach(entry => {if (!entry.isIntersecting && runs.has(entry.target)) stop(entry.target);}); }, {threshold:0});
    document.querySelectorAll('[data-demo]').forEach(figure => sequenceObserver.observe(figure));
    if (!reducedMotion.matches) {
      const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => { if (entry.isIntersecting) {entry.target.classList.add('in-view');revealObserver.unobserve(entry.target);} });
      }, {threshold:0.06, rootMargin:'0px 0px 20px 0px'});
      document.querySelectorAll('.project, .stack, .publication, .awards').forEach(section => {
        // Content already in view stays visible; only later sections enter on scroll.
        if (section.getBoundingClientRect().top > window.innerHeight) {
          section.classList.add('reveal-ready'); revealObserver.observe(section);
        }
      });
    }
  }
})();
