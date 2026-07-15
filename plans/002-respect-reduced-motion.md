# 002 — Respect reduced motion everywhere

- **Status**: DONE
- **Commit**: 360d60b
- **Severity**: HIGH
- **Category**: Accessibility
- **Estimated scope**: 1 file, about 90 CSS/JavaScript lines

## Problem

The reduced-motion rule only changes CSS durations and hides the progress bar:

```css
/* index.html:838-840 — current */
@media (prefers-reduced-motion: reduce) {
  * { animation-duration: 0.01ms !important; transition-duration: 0.01ms !important; }
  .scroll-prog { display: none; }
}
```

That removes useful CSS color/opacity feedback, but it does not affect GSAP. The following motion still runs unconditionally: hero-symbol parallax, section reveals, statistic counters, testimonial scrub, ambient drift, ghost-number parallax, orbit rotation, marquee movement, and JavaScript smooth scrolling.

Representative current code:

```js
/* index.html:1202-1213 — current */
gsap.to('#heroSymbol', {
  yPercent: -30,
  ease: 'none',
  scrollTrigger: {
    trigger: '.hero',
    start: 'top top',
    end: 'bottom top',
    scrub: true,
  }
});

/* index.html:1380-1388 — current */
document.querySelectorAll('.ambient .shape').forEach((s, i) => {
  gsap.to(s, {
    x: 'random(-80, 80)',
    y: 'random(-60, 60)',
    duration: 'random(8, 14)',
    repeat: -1,
    yoyo: true,
    ease: 'sine.inOut',
    delay: i * 0.3,
  });
});
```

Browser verification with `prefers-reduced-motion: reduce` showed the hero transform, ambient shapes, and orbit matrix continuing to change.

## Target

Reduced motion must preserve content and useful opacity/color feedback while removing position changes and perpetual movement.

Replace the current media query with:

```css
/* target */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }

  .reveal-up,
  .reveal-stagger > * {
    opacity: 1;
    transform: none;
  }

  .mobile-nav {
    transform: none;
    transition: opacity 0.2s ease;
  }

  .nav-hamburger span {
    transition: opacity 0.2s ease;
  }

  .nav-links a::after,
  .nav-cta::before,
  .btn.primary::before,
  .cta-btn::before {
    display: none;
  }

  .nav-cta:hover,
  .btn.primary:hover,
  .cta-btn:hover,
  .nav-cta:active,
  .btn.primary:active,
  .btn.ghost:active,
  .cta-btn:active,
  .cta-btn--wa:active,
  .nav-hamburger:active,
  .mobile-nav a:active,
  .btn:hover .arrow {
    transform: none;
  }

  .scroll-prog { display: none; }
}
```

Add one preference source immediately after `gsap.registerPlugin(ScrollTrigger);`:

```js
/* target */
const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
const reduceMotion = motionQuery.matches;
motionQuery.addEventListener('change', () => window.location.reload());
```

The reload ensures a live preference change tears down already-created GSAP timelines instead of leaving perpetual animations running.

Use these exact branches:

```js
/* target reveal behavior */
if (reduceMotion) {
  gsap.set('.reveal-up, .reveal-stagger > *', { opacity: 1, y: 0 });
} else {
  gsap.utils.toArray('.reveal-up').forEach(el => {
    gsap.to(el, {
      opacity: 1, y: 0, duration: 1, ease: 'expo.out',
      scrollTrigger: { trigger: el, start: 'top 85%' }
    });
  });

  gsap.utils.toArray('.reveal-stagger').forEach(group => {
    gsap.to(group.children, {
      opacity: 1, y: 0, duration: 1, ease: 'expo.out', stagger: 0.12,
      scrollTrigger: { trigger: group, start: 'top 80%' }
    });
  });
}
```

For each statistic, write the final value immediately when motion is reduced:

```js
/* target inside the existing .stat loop, after target/suffix are read */
if (reduceMotion) {
  valEl.innerHTML = target + suffix;
  return;
}
```

After the testimonial words are created, use:

```js
/* target */
const words = q.querySelectorAll('.word');
if (reduceMotion) {
  gsap.set(words, { opacity: 1 });
} else {
  gsap.to(words, {
    opacity: 1,
    duration: 0.3,
    stagger: 0.04,
    ease: 'none',
    scrollTrigger: {
      trigger: q,
      start: 'top 80%',
      end: 'bottom 60%',
      scrub: 1,
    }
  });
}
```

All remaining positional/perpetual GSAP blocks must only be created inside `if (!reduceMotion)`: both hero-symbol parallax tweens, scroll progress, ambient shapes, ghost numbers, orbit rotation, and the entire marquee IIFE. Smooth anchor scrolling must use:

```js
window.scrollTo({
  top: y,
  behavior: reduceMotion ? 'auto' : 'smooth'
});
```

## Repo conventions to follow

- Keep the existing GSAP and ScrollTrigger CDN integration; no new library is needed.
- Keep the existing `expo.out` reveal convention for users without reduced motion.
- Keep opacity feedback at the audit's exact reduced-motion example value: `0.2s ease`.
- Execute Plans 003, 004, and 005 first. They remove the hero entrance, scramble, cursor, magnetic buttons, tilt, and CTA wave, then add compositor-safe hover/press feedback. This plan must not recreate removed effects and must override Plan 005's movement under reduced motion while retaining color/opacity feedback.

## Steps

1. Confirm Plans 003, 004, and 005 are complete.
2. Replace the universal `0.01ms` reduced-motion rule with the exact targeted CSS media query above. Keep this media query after Plan 005's fine-pointer hover query so the reduced-motion overrides win.
3. Add `motionQuery`, `reduceMotion`, and the change listener immediately after GSAP registration.
4. Wrap both hero-symbol parallax tweens in one `if (!reduceMotion)` block.
5. Replace the two reveal loops with the exact reduced/no-preference branch above.
6. In the statistics loop, set the final value and `return` before creating ScrollTrigger when `reduceMotion` is true.
7. In the quote IIFE, cache `words` and choose immediate full opacity versus the existing scrub tween.
8. Only create scroll-progress, ambient-shape, ghost-number, orbit, and marquee animations when `reduceMotion` is false.
9. Change JavaScript anchor scrolling to `auto` under reduced motion.
10. Search the file for every `repeat: -1`, `scrub:`, and `behavior: 'smooth'`; confirm each is either guarded by `!reduceMotion` or branched as specified.

## Boundaries

- Execute only after Plans 003, 004, and 005.
- Do NOT remove the static marquee content, ambient shapes, orbit label, hero symbol, testimonial text, or statistics.
- Do NOT disable all transitions globally.
- Do NOT hide content under reduced motion.
- Do NOT add dependencies or persist the preference yourself; use the operating-system media query.
- If the expected blocks differ after the prerequisite plans, STOP and report drift rather than reintroducing removed effects.

## Verification

- **Mechanical**: run `git diff --check`. Run `rg -n "repeat: -1|scrub:|behavior:" index.html` and manually confirm every result is guarded/branched. Run `rg -n "0\\.01ms|transition-duration: 0" index.html`; it must return no matches.
- **Feel check**: serve with `python3 -m http.server 4173`. In Chrome DevTools Rendering, emulate `prefers-reduced-motion: reduce`, then reload.
  - Hero and section content must be immediately readable.
  - Ambient blobs, ghost numbers, hero symbol, orbit, marquee, and progress bar must not move.
  - Statistics must show final values without counting.
  - The testimonial must be fully opaque without scroll scrubbing.
  - Opening the mobile menu must retain a 200ms opacity fade but no animated positional movement.
  - Hovering or pressing buttons must not translate, scale, sweep an underline, move an arrow, or run a sheen; color/opacity feedback must remain.
  - Anchor navigation must jump directly instead of smooth-scrolling.
  - Switch back to `no-preference`, reload, and confirm the retained marketing motion still works.
- **Done when**: reduced-motion users receive no positional, scroll-linked, or perpetual motion while useful opacity/color feedback remains.
