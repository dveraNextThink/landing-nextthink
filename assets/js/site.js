(() => {
  document.documentElement.classList.add('js');

  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.mobile-toggle');
  const panel = document.querySelector('.mobile-panel');

  const updateHeader = () => {
    header?.classList.toggle('scrolled', window.scrollY > 8);
  };

  const closeMenu = ({ restoreFocus = false } = {}) => {
    if (!toggle || !panel) return;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', 'Abrir menú');
    panel.classList.remove('open');
    document.body.style.overflow = '';
    if (restoreFocus) toggle.focus();
  };

  const openMenu = () => {
    if (!toggle || !panel) return;
    toggle.setAttribute('aria-expanded', 'true');
    toggle.setAttribute('aria-label', 'Cerrar menú');
    panel.classList.add('open');
    document.body.style.overflow = 'hidden';
    window.setTimeout(() => panel.querySelector('a')?.focus(), 230);
  };

  toggle?.addEventListener('click', () => {
    const isOpen = toggle.getAttribute('aria-expanded') === 'true';
    isOpen ? closeMenu() : openMenu();
  });

  panel?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => closeMenu());
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
      closeMenu({ restoreFocus: true });
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) closeMenu();
  }, { passive: true });

  window.addEventListener('scroll', updateHeader, { passive: true });
  updateHeader();

  const year = document.querySelector('[data-current-year]');
  if (year) year.textContent = String(new Date().getFullYear());
})();
