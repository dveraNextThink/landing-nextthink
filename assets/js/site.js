(() => {
  const root = document.documentElement;
  root.classList.add('js');

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

  document.querySelectorAll('[data-current-year]').forEach((year) => {
    year.textContent = String(new Date().getFullYear());
  });

  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (motionQuery.matches) return;

  const motionItems = new Set();
  const observers = [];
  const animations = [];
  const motionCleanups = [];

  const revealEntries = [];
  const addRevealEntry = (trigger, items) => {
    const uniqueItems = [...new Set(items)].filter((item) => !motionItems.has(item));
    if (!trigger || uniqueItems.length === 0) return;

    uniqueItems.forEach((item, index) => {
      motionItems.add(item);
      item.classList.add('motion-item', 'motion-pending');
      item.style.setProperty('--motion-delay', `${Math.min(index, 4) * 60}ms`);
    });
    revealEntries.push({ trigger, items: uniqueItems });
  };

  const prepareReveals = () => {
    const groupSelectors = [
      '.card-grid',
      '.process-list',
      '.stats-grid',
      '.feature-grid',
      '.deliverables',
      '.contact-grid',
      '.footer-grid',
    ];

    groupSelectors.forEach((selector) => {
      document.querySelectorAll(selector).forEach((group) => {
        addRevealEntry(group, [...group.children]);
      });
    });

    const individualSelectors = [
      '.section-head',
      '.split',
      '.case-feature',
      '.cta-section .wrap',
    ];

    individualSelectors.forEach((selector) => {
      document.querySelectorAll(selector).forEach((group) => {
        addRevealEntry(group, [...group.children]);
      });
    });

    if (revealEntries.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const revealEntry = revealEntries.find((item) => item.trigger === entry.target);
        revealEntry?.items.forEach((item) => item.classList.remove('motion-pending'));
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -7% 0px' });

    observers.push(observer);
    root.classList.add('motion-ready');
    requestAnimationFrame(() => {
      revealEntries.forEach(({ trigger }) => observer.observe(trigger));
    });
  };

  const prepareQuoteReveal = () => {
    document.querySelectorAll('.case-feature blockquote').forEach((quote) => {
      const walker = document.createTreeWalker(quote, NodeFilter.SHOW_TEXT);
      const textNodes = [];
      while (walker.nextNode()) textNodes.push(walker.currentNode);

      let wordIndex = 0;
      textNodes.forEach((textNode) => {
        if (!textNode.textContent?.trim()) return;
        const fragment = document.createDocumentFragment();
        textNode.textContent.split(/(\s+)/).forEach((part) => {
          if (!part.trim()) {
            fragment.append(part);
            return;
          }
          const span = document.createElement('span');
          span.className = 'motion-word';
          span.style.setProperty('--word-index', String(wordIndex++));
          span.textContent = part;
          fragment.append(span);
        });
        textNode.replaceWith(fragment);
      });

      quote.classList.add('motion-quote');
      const observer = new IntersectionObserver(([entry]) => {
        if (!entry?.isIntersecting) return;
        quote.classList.add('is-visible');
        observer.disconnect();
      }, { threshold: 0.35 });
      observers.push(observer);
      observer.observe(quote);
    });
  };

  const prepareScramble = () => {
    if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;

    document.querySelectorAll('[data-scramble]').forEach((element) => {
      const original = element.dataset.scramble || element.textContent.trim();
      const characters = '!@#$%^&*<>-_=+[]{}abcdefghijklmnopqrstuvwxyz';
      let frameId = 0;

      const restore = () => {
        cancelAnimationFrame(frameId);
        element.classList.remove('is-scrambling');
        element.removeAttribute('data-scramble-frame');
      };

      const scramble = () => {
        restore();
        const startAt = performance.now();
        element.classList.add('is-scrambling');

        const update = (now) => {
          const progress = Math.min(1, (now - startAt) / 600);
          const revealed = Math.floor(progress * original.length);
          const frame = [...original].map((character, index) => {
            if (index < revealed || character === ' ') return character;
            return characters[Math.floor(Math.random() * characters.length)];
          }).join('');
          element.setAttribute('data-scramble-frame', frame);

          if (progress < 1) {
            frameId = requestAnimationFrame(update);
          } else {
            restore();
          }
        };

        frameId = requestAnimationFrame(update);
      };

      element.addEventListener('pointerenter', scramble);
      element.addEventListener('pointerleave', restore);
      motionCleanups.push(() => {
        restore();
        element.removeEventListener('pointerenter', scramble);
        element.removeEventListener('pointerleave', restore);
      });
    });
  };

  const prepareMarquee = () => {
    const band = document.querySelector('.logo-band');
    const track = band?.querySelector('.logo-grid');
    if (!band || !track || track.children.length < 2) return;

    const originals = [...track.children];
    originals.forEach((item) => {
      const clone = item.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      clone.setAttribute('alt', '');
      clone.setAttribute('data-motion-clone', '');
      clone.removeAttribute('loading');
      track.append(clone);
    });
    band.classList.add('motion-marquee');

    requestAnimationFrame(() => {
      const firstClone = track.children[originals.length];
      const distance = firstClone.offsetLeft - track.children[0].offsetLeft;
      if (distance <= 0) return;
      const animation = track.animate([
        { transform: 'translate3d(0, 0, 0)' },
        { transform: `translate3d(-${distance}px, 0, 0)` },
      ], {
        duration: 36000,
        iterations: Infinity,
        easing: 'linear',
      });
      animations.push(animation);
    });
  };

  const prepareScrollMotion = () => {
    const progress = document.createElement('div');
    progress.className = 'scroll-progress';
    progress.setAttribute('aria-hidden', 'true');
    document.body.append(progress);

    const hero = document.querySelector('.hero');
    const heroMark = hero?.querySelector('.hero-mark');
    const heroImage = heroMark?.querySelector('img');
    let ticking = false;

    const update = () => {
      const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
      const scrollProgress = maxScroll > 0 ? window.scrollY / maxScroll : 0;
      progress.style.transform = `scaleX(${Math.max(0, Math.min(1, scrollProgress))})`;

      if (hero && heroMark && heroImage) {
        const heroProgress = Math.max(0, Math.min(1, window.scrollY / Math.max(hero.offsetHeight, 1)));
        heroMark.style.transform = `translate3d(0, calc(-50% + ${heroProgress * -72}px), 0)`;
        heroImage.style.transform = `rotate(${heroProgress * 42}deg)`;
      }
      ticking = false;
    };

    const requestUpdate = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(update);
    };

    window.addEventListener('scroll', requestUpdate, { passive: true });
    window.addEventListener('resize', requestUpdate, { passive: true });
    motionCleanups.push(() => {
      window.removeEventListener('scroll', requestUpdate);
      window.removeEventListener('resize', requestUpdate);
    });
    requestUpdate();
  };

  const disableMotion = () => {
    observers.forEach((observer) => observer.disconnect());
    animations.forEach((animation) => animation.cancel());
    motionCleanups.forEach((cleanup) => cleanup());
    root.classList.remove('motion-ready');
    document.querySelectorAll('.motion-pending').forEach((item) => item.classList.remove('motion-pending'));
    document.querySelectorAll('.motion-quote').forEach((quote) => quote.classList.add('is-visible'));
    document.querySelectorAll('[data-motion-clone]').forEach((clone) => clone.remove());
    document.querySelector('.logo-band.motion-marquee')?.classList.remove('motion-marquee');
    document.querySelector('.hero-mark')?.removeAttribute('style');
    document.querySelector('.hero-mark img')?.removeAttribute('style');
    document.querySelector('.scroll-progress')?.remove();
  };

  try {
    prepareReveals();
    prepareQuoteReveal();
    prepareScramble();
    prepareMarquee();
    prepareScrollMotion();
  } catch (error) {
    disableMotion();
    console.error('No se pudo iniciar la capa de movimiento.', error);
  }

  motionQuery.addEventListener?.('change', (event) => {
    if (event.matches) disableMotion();
  });
})();
